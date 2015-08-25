# -*- coding: utf-8 -*-

from rer.cookieconsent.testing import COOKIECONSENT_INTEGRATION_TESTING
from rer.cookieconsent.tests.base import BaseTestCase
from rer.cookieconsent.tests.base import optout_generator
from zope.component import getMultiAdapter
from rer.cookieconsent import config
from DateTime import DateTime


class DashboardTestCase(BaseTestCase):
    """Tests cookies behaviors"""
    
    layer = COOKIECONSENT_INTEGRATION_TESTING
    
    def setUp(self):
        self.markRequestWithLayer()
        self.populateConfig()
        self.date = DateTime() + 1
        request = self.layer['request']
        request['ACTUAL_URL'] = 'http://plone/@@optout-dashboard'

    def populateConfig(self):
        settings = self.getSettings()
        settings.optout_configuration = (
                                         optout_generator('foo', ('foo1', 'foo2')),
                                         optout_generator('bar', ('bar',))
                                         )

    def test_basic_behavior(self):
        portal = self.layer['portal']
        request = self.layer['request']
        request.form['form.submitted'] = 1
        request.form['accept_cookies'] = 'true'
        request.form['app_foo'] = 'true'
        request.form['app_bar'] = 'false'
        view = getMultiAdapter((portal, request), name=u"optout-dashboard")
        view()
        cookies = request.response.cookies
        self.assertTrue(config.COOKIECONSENT_NAME in cookies)
        self.assertEqual(cookies[config.COOKIECONSENT_NAME]['value'], 'true')
        self.assertTrue('foo1-optout' in cookies)
        self.assertEqual(cookies['foo1-optout']['value'], 'true')
        self.assertTrue('foo2-optout' in cookies)
        self.assertEqual(cookies['foo1-optout']['value'], 'true')
        self.assertTrue('bar-optout' in cookies)
        self.assertEqual(cookies['bar-optout']['value'], 'false')

    def test_true_global_settings_force_optout(self):
        portal = self.layer['portal']
        request = self.layer['request']
        request.form['form.submitted'] = 1
        view = getMultiAdapter((portal, request), name=u"optout-dashboard")
        view()
        cookies = request.response.cookies
        self.assertTrue(config.COOKIECONSENT_NAME in cookies)
        self.assertEqual(cookies[config.COOKIECONSENT_NAME]['value'], 'false')
        self.assertTrue('foo1-optout' in cookies)
        self.assertEqual(cookies['foo1-optout']['value'], 'true')
        self.assertTrue('foo2-optout' in cookies)
        self.assertEqual(cookies['foo1-optout']['value'], 'true')
        self.assertTrue('bar-optout' in cookies)
        self.assertEqual(cookies['bar-optout']['value'], 'true')

