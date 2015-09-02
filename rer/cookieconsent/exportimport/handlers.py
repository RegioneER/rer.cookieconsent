# -*- coding: utf-8 -*-

from zope.interface import implements
from zope.component import adapts
from zope.component import getSiteManager
from zope.component import queryMultiAdapter
from zope.component.interfaces import IComponentRegistry
from Products.GenericSetup.interfaces import IBody
from Products.GenericSetup.interfaces import ISetupEnviron
from Products.GenericSetup.utils import XMLAdapterBase
from Products.CMFCore.utils import getToolByName
from rer.cookieconsent import logger
from plone.registry.interfaces import IRegistry
from zope.component import queryUtility
from rer.cookieconsent.controlpanel.interfaces import ICookieConsentSettings
from rer.cookieconsent.controlpanel.interfaces import OptOutEntry
from rer.cookieconsent.controlpanel.interfaces import OptOutEntrySubitem
from rer.cookieconsent.controlpanel.interfaces import CookieBannerEntry


class CookieConsentXMLAdapter(XMLAdapterBase):
    """In- and exporter for a local custom menu configuration
    """
    implements(IBody)
    adapts(IComponentRegistry, ISetupEnviron)

    name = 'cookieconsent'
    _LOGGER_ID = 'rer.cookieconsent'


    def _exportNode(self):
        """Export cookie consent configuration
        """
        raise NotImplementedError("Export is not available right now")

    def _importNode(self, node):
        """Import cookie consent configuration
        """
        self._configure(node)
        self._logger.info('Cookie consent configuration imported')

    def nodedata(self, node):
        """Given a node, returns tagName and property "name" if exists"""
        tagName = getattr(node, 'tagName', '').lower()
        name = node.getAttribute('name').lower() if tagName else None
        return tagName, name

    def _configure(self, node):
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(ICookieConsentSettings, check=False)
        
        for child in node.childNodes:
            tagName, name = self.nodedata(child)
            if tagName=='property' and name.lower()=='accept-on-click':
                 settings.accept_on_click = self._getNodeText(child).lower()=='true'
            elif tagName=='cookie_consent_configuration':
                purge = child.getAttribute('purge').lower() or 'true'
                if purge=='true':
                    settings.cookie_consent_configuration = tuple()
                for subnode in child.childNodes:
                    if subnode.nodeType != subnode.ELEMENT_NODE:
                         continue
                    self._configureCookieConsentBanner(subnode, settings)
            elif tagName=='optout_configuration':
                purge = child.getAttribute('purge').lower() or 'true'
                if purge=='true':
                    settings.optout_configuration = tuple()
                for subnode in child.childNodes:
                    if subnode.nodeType != subnode.ELEMENT_NODE:
                         continue
                    self._configureOptOut(subnode, settings)

    def _configureCookieConsentBanner(self, node, settings):
        """Set an ICookieBannerEntry entry in the registry
        """
        bannerconf = CookieBannerEntry()
        for child in node.childNodes:
            tagName, name = self.nodedata(child)
            if name in ('lang', 'text', 'privacy-link-url', 'privacy-link-text', 'dashboard-link-text'):
                if name=='lang':
                    # check if the language is valid for that site
                    lang = self._getNodeText(child).decode('utf-8')
                    lang_tool =  getToolByName(self.context, 'portal_languages')
                    if lang not in lang_tool.getSupportedLanguages():
                        logger.info("Can't configure %s language in that site" % lang)
                        return
                setattr(bannerconf, name.replace('-', '_'),
                        self._getNodeText(child).decode('utf-8'))
        settings.cookie_consent_configuration += (bannerconf,)

    def _configureOptOut(self, node, settings):
        """Set an IOptOutEntry entry in the registry
        """
        optoutconf = OptOutEntry()
        for child in node.childNodes:
            tagName, name = self.nodedata(child)
            if name=='app-id':
                optoutconf.app_id = self._getNodeText(child).encode('utf-8')
            elif name=='cookies':
                optoutconf.cookies = tuple(self._getValues(child))
            elif name=='default-value':
                optoutconf.default_value = self._getNodeText(child).encode('utf-8').lower()
            elif tagName=='optout_configuration_ui':
                optoutconf.texts = tuple(self._getOptOutUITexts(child))
        settings.optout_configuration += (optoutconf,)

    def _getOptOutUITexts(self, node):
        results = []
        # this must be a sequence of object tags
        for child in node.childNodes:
            tagName, name = self.nodedata(child)
            if not tagName:
                continue
            optout_ui_conf = OptOutEntrySubitem()
            # this must be a sequence of properties with values
            for child in child.childNodes:
                tagName, name = self.nodedata(child)
                if name in ('lang', 'app-title', 'app-description'):
                    setattr(optout_ui_conf, name.replace('-', '_'), self._getNodeText(child))
            results.append(optout_ui_conf)
        return results

    def _getValues(self, node):
        """Returns a list of inner <element>s 
        """
        results = []
        for child in node.childNodes:
            value = self._getNodeText(child).strip()
            if not value:
                continue
            results.append(value.encode('utf-8'))
        return results


def importCookieConsentSettings(context):
    """Import cookies consent configurations
    """
    sm = getSiteManager(context.getSite())
    if sm is None or not IComponentRegistry.providedBy(sm):
        logger.info("Can not register components - no site manager found.")
        return

    importer = queryMultiAdapter((sm, context), IBody,
                                  name=u'rer.cookieconsent')
    if importer:
        filename = '%s%s' % (importer.name, importer.suffix)
        body = context.readDataFile(filename)
        if body is not None:
            importer.filename = filename  # for error reporting
            importer.body = body
