# -*- coding: utf-8 -*-

import urlparse
from DateTime import DateTime
#from ZPublisher.interfaces import IPubBeforeCommit, IPubSuccess
from plone.browserlayer.utils import registered_layers
from plone.registry.interfaces import IRegistry
from rer.cookieconsent import config 
from rer.cookieconsent.controlpanel.interfaces import ICookieConsentSettings
from rer.cookieconsent.interfaces import ICookieConsentLayer
from zope.component import queryUtility
from zope.component.hooks import getSite
from rer.cookieconsent.utils import setCookie
from rer.cookieconsent import config


#@adapter(IPubSuccess)
def send_initial_cookies_values(event):
    """ If the COOKIECONSENT_NAME if not present at all, user not choosen yet if accept cookies or not.
    In that case we automatically send all of the opt-put cookies not present.
    """

    # Checks to limit subscribers calls
    if ICookieConsentLayer not in registered_layers():
        return
    site = getSite()
    if site==None:
        return

    request = event.request
    if config.COOKIECONSENT_NAME in request.response.cookies:
        return
    # TODO: evaluate if move this list in a Plone registry field (performance?)
    for subdomain in config.DOMAIN_WHITELIST:
        if urlparse.urlparse(request.URL).netloc.find(subdomain)>-1:
            return

    optout_all(request, 'true')

    
def optout_all(request, value, update=False):
    """
    For all of the opt-out cookies, set the value
    This will not change values for cookies already set until update=True is provided
    """
    registry = queryUtility(IRegistry)
    settings = registry.forInterface(ICookieConsentSettings)
    for oo_conf in settings.optout_configuration:
        for cookie in oo_conf.cookies:
            cookiename = "%s-optout" % cookie
            if cookiename in request.cookies and not update:
                continue
            nextYear = DateTime() + 365
            setCookie(request.response, cookiename, value, expires=nextYear.rfc822())
