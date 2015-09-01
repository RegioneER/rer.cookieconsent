# -*- coding: utf-8 -*-

from zope.component.hooks import getSite
from DateTime import DateTime


def setCookie(response, name, value, **kwargs):
    site = getSite()
    response.setCookie(name, value,
                       path=kwargs.get('path') or site.absolute_url_path(),
                       expires=kwargs.get('expires') or (DateTime()+365).rfc822(),
                       http_only=kwargs.get('http_only') or False) # HttpOnly true blocks client side work
