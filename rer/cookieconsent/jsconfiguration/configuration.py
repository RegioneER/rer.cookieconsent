# -*- coding: utf-8 -*-

from collective.jsconfiguration.interfaces import IJSONDataProvider
from collective.regjsonify.interfaces import IJSONifier
from plone.registry.interfaces import IRegistry
from rer.cookieconsent.utils import get_url_to_dashboard
from rer.cookieconsent.controlpanel.interfaces import ICookieConsentSettings
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from zope.component import queryUtility
from zope.component import getMultiAdapter
from zope.interface import implementer


@implementer(IJSONDataProvider)
class JSONConfigurationAdapter(object):

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.view = view

    def __call__(self):
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(ICookieConsentSettings)
        portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        site = portal_state.portal()
        data_settings = IJSONifier(settings).json()
        data_settings['actual_url'] = self.request['ACTUAL_URL']
        data_settings['here_url'] = self.context.absolute_url()
        data_settings['dashboard_url'] = get_url_to_dashboard()
        data_settings['portal_path'] = site.absolute_url_path()
        return data_settings


@implementer(IJSONDataProvider)
class DOMConfigurationAdapter(object):

    template = ViewPageTemplateFile('banner-configuration-labels.pt')

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.view = view

    def __call__(self):
        return self.template()
