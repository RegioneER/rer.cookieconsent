# -*- coding: utf-8 -*-

from rer.cookieconsent.testing import COOKIECONSENT_INTEGRATION_TESTING
from rer.cookieconsent.tests.base import BaseTestCase
from rer.cookieconsent.tests.base import optout_generator
from zope.component import getMultiAdapter
from rer.cookieconsent.init_cookies import send_initial_cookies_values
from rer.cookieconsent import config


def raiseFakeEvent(request):
    """Trigger the cookie subscriber manually"""

    class FakeEvent(object):
        def __init__(self,request):
            self.request = request

    fe = FakeEvent(request)
    send_initial_cookies_values(fe)


class CoockiesTestCase(BaseTestCase):
    """Tests cookies behaviors"""
    
    layer = COOKIECONSENT_INTEGRATION_TESTING
    
    def setUp(self):
        self.markRequestWithLayer()
        self.populateConfig()
        request = self.layer['request']
        request['ACTUAL_URL'] = 'http://plone/@@sharing'

    def populateConfig(self):
        settings = self.getSettings()
        settings.optout_configuration = (
                                         optout_generator('foo', ('foo1', 'foo2')),
                                         optout_generator('bar', ('bar',))
                                         )
    
    def test_first_access(self):
        """Tests that on first access we have no cookieconsent cookie but all of the opt-out ones"""
        portal = self.layer['portal']
        request = self.layer['request']
        raiseFakeEvent(request)
        view = getMultiAdapter((portal, request), name=u"sharing")
        view()
        cookies = request.response.cookies
        self.assertFalse(config.COOKIECONSENT_NAME in cookies)
        self.assertTrue('foo1-optout' in cookies)
        self.assertEqual(cookies['foo1-optout']['value'], 'true')
        self.assertTrue('foo2-optout' in cookies)
        self.assertEqual(cookies['foo2-optout']['value'], 'true')
        self.assertTrue('bar-optout' in cookies)
        self.assertEqual(cookies['bar-optout']['value'], 'true')
