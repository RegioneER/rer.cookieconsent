# -*- coding: utf-8 -*-

from rer.cookieconsent import config 
from zope.interface import Interface
from DateTime import DateTime
#from ZPublisher.interfaces import IPubBeforeCommit, IPubSuccess
from zope.component.hooks import getSite
from plone.browserlayer.utils import registered_layers
from rer.cookieconsent.interfaces import ICookieConsentLayer
from plone.registry.interfaces import IRegistry
from rer.cookieconsent.controlpanel.interfaces import ICookieConsentSettings
from zope.component import queryUtility


#@adapter(IPubSuccess)
def send_initial_cookies_values(event):
    """ If the COOKIECONSENT_NAME if not present at all, use not choose if
    accept cookies or not.
    In that case we automatically send all of the optput cookies not present.
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

    optout_all(request, 'true')

    
def optout_all(request, value, update=False):
    """
    For all of the opt-out cookies, set the value
    This will not change values for cookies already set until update=True is provided
    """
    site = getSite()
    registry = queryUtility(IRegistry)
    settings = registry.forInterface(ICookieConsentSettings)
    for oo_conf in settings.optout_configuration:
        for cookie in oo_conf.cookies:
            cookiename = "%s-optout" % cookie
            if cookiename in request.cookies and not update:
                continue
            nextYear = DateTime() + 365
            request.response.setCookie(cookiename, value,
                                       path='/'.join(site.getPhysicalPath()),
                                       expires=nextYear.rfc822())
