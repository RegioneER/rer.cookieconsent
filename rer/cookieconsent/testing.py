# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from zope.configuration import xmlconfig


class CookieConsentPanel(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import rer.cookieconsent
        import collective.regjsonify
        xmlconfig.file('configure.zcml',
                       collective.regjsonify,
                       context=configurationContext)
        # xmlconfig registration below only needed for Plone 4.2 compatibility
        xmlconfig.file('configure.zcml',
                       rer.cookieconsent,
                       context=configurationContext)
        z2.installProduct(app, 'rer.cookieconsent')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'rer.cookieconsent:default')
        #quickInstallProduct(portal, 'rer.cookieconsent')


COOKIECONSENT_FIXTURE = CookieConsentPanel()
COOKIECONSENT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COOKIECONSENT_FIXTURE, ),
    name="CookieConsent:Integration",
)
COOKIECONSENT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COOKIECONSENT_FIXTURE, ),
    name="CookieConsent:Functional",
)

COOKIECONSENT_ROBOT_TESTING = FunctionalTesting(
    bases=(
        COOKIECONSENT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE),
    name="CookieConsent:Robot")
