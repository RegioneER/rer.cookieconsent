# -*- coding: utf-8 -*-

from zope.component.hooks import getSite
from DateTime import DateTime
from plone.app.layout.navigation.interfaces import INavigationRoot
from zope.component import getMultiAdapter


def setCookie(response, name, value, **kwargs):
    site = getSite()
    response.setCookie(name, value,
                       path=kwargs.get('path') or site.absolute_url_path(),
                       expires=kwargs.get('expires') or (DateTime()+365).rfc822(),
                       http_only=kwargs.get('http_only') or False) # HttpOnly true blocks client side work


def get_url_to_dashboard():
    """URL to dashboard depends on i18n settings in the site
    """
    site = getSite()
    portal_state = getMultiAdapter((site, site.REQUEST), name=u'plone_portal_state')
    current_language = portal_state.language()
    lang_root_folder = getattr(site, current_language, None)
    if lang_root_folder and INavigationRoot.providedBy(lang_root_folder):
        return "%s/@@optout-dashboard" % lang_root_folder.absolute_url()
    return "%s/@@optout-dashboard" % site.absolute_url()
