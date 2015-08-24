# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from plone.registry.interfaces import IRegistry
from rer.cookieconsent.controlpanel.interfaces import ICookieConsentSettings
from zope.component import queryUtility


class ResetOptoutView(BrowserView):
    """Remove all of the optout cookies"""

    def __call__(self, *args, **kwargs):
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(ICookieConsentSettings)
        for oo_conf in settings.optout_configuration:
            for cookie in oo_conf.cookies:
                if self.request.cookies.get("%s-optout" % cookie):
                    del self.request.cookies["%s-optout" % cookie]

        back_to = self.request.form.get('came_from') or self.context.absolute_url()
        self.request.response.redirect(back_to)
