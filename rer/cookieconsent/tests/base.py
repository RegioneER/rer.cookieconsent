# -*- coding: utf-8 -*-

import unittest
from zope import interface
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry
from rer.cookieconsent.interfaces import ICookieConsentLayer
from rer.cookieconsent.controlpanel.interfaces import ICookieConsentSettings
from rer.cookieconsent.controlpanel.interfaces import OptOutEntry
from rer.cookieconsent.controlpanel.interfaces import OptOutEntrySubitem


class BaseTestCase(unittest.TestCase):

    def getSettings(self):
        registry = queryUtility(IRegistry)
        return registry.forInterface(ICookieConsentSettings, check=False)

    def markRequestWithLayer(self):
        # to be removed when p.a.testing will fix https://dev.plone.org/ticket/11673
        request = self.layer['request']
        interface.alsoProvides(request, ICookieConsentLayer)


def optout_generator(app_id, cookies, title=u'', description=u''):
    return OptOutEntry(app_id=app_id, cookies=cookies,
                       texts=(OptOutEntrySubitem(lang=u'en', app_title=title, app_description=description),))
