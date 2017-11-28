# -*- coding: utf-8 -*-

from DateTime import DateTime
from plone import api
from plone.app.layout.navigation.interfaces import INavigationRoot
from zope.component import getMultiAdapter


def setCookie(response, name, value, **kwargs):
    site = api.portal.get()
    response.setCookie(
        name,
        value,
        path=kwargs.get('path') or site.absolute_url_path(),
        expires=kwargs.get('expires') or (DateTime()+365).rfc822(),
        http_only=kwargs.get('http_only') or False)
    # HttpOnly true blocks client side work


def get_url_to_dashboard():
    """URL to dashboard depends on i18n settings in the site
    """
    site = api.portal.get()
    portal_state = getMultiAdapter(
        (site, site.REQUEST), name=u'plone_portal_state')
    current_language = portal_state.language()
    lang_root_folder = getattr(site, current_language, None)
    if lang_root_folder and INavigationRoot.providedBy(lang_root_folder):
        return '{0}/@@optout-dashboard'.format(lang_root_folder.absolute_url())
    return '{0}/@@optout-dashboard'.format(site.absolute_url())
