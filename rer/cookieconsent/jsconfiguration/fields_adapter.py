# -*- coding: utf-8 -*-

import re
from collective.regjsonify.interfaces import IJSONFieldDumper
from collective.regjsonify.fields import Object
from zope.component.hooks import getSite
from zope.interface import implementer
from rer.cookieconsent.utils import get_url_to_dashboard
from plone import api


URL_MODEL = '<a href="{0}">{1}</a>{2}'
pattern_privacy_link = re.compile(r'(\$privacy_link)(\W|$)')
pattern_privacy_link_url = re.compile(r'(\$privacy_link_url)(\W|$)')
pattern_privacy_link_text = re.compile(r'(\$privacy_link_text)(\W|$)')
pattern_dashboard_link = re.compile(r'(\$dashboard_link)(\W|$)')
pattern_dashboard_link_url = re.compile(r'(\$dashboard_link_url)(\W|$)')
pattern_dashboard_link_text = re.compile(r'(\$dashboard_link_text)(\W|$)')


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
        privacy_link_text = result['privacy_link_text'] or privacy_link_url

        dashboard_link_url = get_url_to_dashboard()
        dashboard_link_text = result['dashboard_link_text'] or dashboard_link_url

        # privacy link
        new_text = pattern_privacy_link.sub(URL_MODEL.format(privacy_link_url,
                                                             privacy_link_text,
                                                             r'\2'),
                                    new_text)
        new_text = pattern_privacy_link_url.sub(privacy_link_url + r'\2', new_text)
        new_text = pattern_privacy_link_text.sub(privacy_link_text + r'\2', new_text)

        # opt-out dashboard link
        new_text = pattern_dashboard_link.sub(URL_MODEL.format(dashboard_link_url,
                                                               dashboard_link_text,
                                                             r'\2'),
                                    new_text)
        new_text = pattern_dashboard_link_url.sub(dashboard_link_url + r'\2', new_text)
        new_text = pattern_dashboard_link_text.sub(dashboard_link_text + r'\2', new_text)

        new_text = new_text.strip().replace("\n", "<br />\n")
        result['text'] = self.cleanHTML(new_text)
        result['privacy_link_url'] = privacy_link_url
        del result['privacy_link_text']
        del result['dashboard_link_text']
        return result

    def cleanHTML(self, text):
        """
        clean text in the given data, so the user can't insert dangerous
        html (for example cross-site scripting)
        """
        pt = api.portal.get_tool('portal_transforms')
        safe_text = pt.convert('safe_html', text)
        return safe_text.getData()

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
