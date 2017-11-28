# -*- coding: utf-8 -*-
from plone import api


DEFAULT_PROFILE = 'profile-rer.cookieconsent:default'


def to_2000(context):
    'Import new bundle and remove old resources'
    setup_tool = api.portal.get_tool('portal_setup')
    setup_tool.runImportStepFromProfile(DEFAULT_PROFILE, 'plone.app.registry')
    setup_tool.runAllImportStepsFromProfile(
        'profile-rer.cookieconsent:to_2000')
