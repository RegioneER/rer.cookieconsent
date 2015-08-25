# -*- coding: utf-8 -*-

import re
from collective.regjsonify.interfaces import IJSONFieldDumper
from collective.regjsonify.fields import Object
from zope.component.hooks import getSite
from zope.interface import implementer


URL_MODEL = '<a href="{0}">{1}</a>{2}'
pattern_link = re.compile(r'(\$privacy_link)(\W|$)')
pattern_link_url = re.compile(r'(\$privacy_link_url)(\W|$)')
pattern_link_text = re.compile(r'(\$privacy_link_text)(\W|$)')


@implementer(IJSONFieldDumper)
class CookieBannerSettingsAdapter(Object):
    """
    collective.regjsonify implementation for ICookieBannerEntry
    
    Like basic Object adapter but we need to perfomr some string interpolation.
    Also, some server-side only resources are removed. 
    """
    
    def __init__(self, field):
        self.field = field

    def data(self, record):
        result = super(CookieBannerSettingsAdapter, self).data(record)
        new_text = result['text']

        # privacy_link_url can be a document path, not an URL
        privacy_link_url = result['privacy_link_url']
        if privacy_link_url.startswith('/'):
            site = getSite()
            privacy_link_url = site.absolute_url() + privacy_link_url

        new_text = pattern_link.sub(URL_MODEL.format(privacy_link_url,
                                                     result['privacy_link_text'],
                                                     r'\2'),
                                    new_text)
        new_text = pattern_link_url.sub(privacy_link_url + r'\2', new_text)
        new_text = pattern_link_text.sub(result['privacy_link_text'] + r'\2', new_text)
        new_text = new_text.strip().replace("\n", "<br />\n")
        result['text'] = new_text
        result['privacy_link_url'] = privacy_link_url
        del result['privacy_link_text']
        return result


@implementer(IJSONFieldDumper)
class OptOutSettingsAdapter(Object):
    """
    collective.regjsonify implementation for ICookieBannerSettingsAdapter.
    Do not return anything 
    """

    def __init__(self, field):
        self.field = field

    def data(self, record):
        result = super(CookieBannerSettingsAdapter, self).data(record)
        del result['optout_configuration']
        return result
