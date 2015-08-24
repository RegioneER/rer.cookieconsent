# -*- coding: utf-8 -*-

from operator import itemgetter
from plone.app.vocabularies.language import AvailableContentLanguageVocabulary
from zope.site.hooks import getSite
from Products.CMFCore.utils import getToolByName
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class SupportedContentLanguageVocabulary(AvailableContentLanguageVocabulary):

    def __call__(self, context):
        items = []
        site = getSite()
        ltool = getToolByName(site, 'portal_languages', None)
        if ltool is not None:
            items = ltool.listSupportedLanguages()
            items.sort(key=itemgetter(1))
            items = [SimpleTerm(i[0].decode('utf-8'), i[0].decode('utf-8'), i[1].decode('utf-8')) for i in items]
        return SimpleVocabulary(items)


SupportedContentLanguageVocabularyFactory = SupportedContentLanguageVocabulary()