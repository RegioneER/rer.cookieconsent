# -*- coding: utf-8 -*-
from DateTime import DateTime
from plone import api
from plone.memoize.view import memoize
from plone.registry.interfaces import IRegistry
from Products.Five.browser import BrowserView
from rer.cookieconsent import messageFactory as _
from rer.cookieconsent import config
from rer.cookieconsent.controlpanel.interfaces import ICookieConsentSettings
from rer.cookieconsent.init_cookies import optout_all
from rer.cookieconsent.utils import setCookie
from zope.component import getMultiAdapter
from zope.component import queryUtility
from zope.i18n import translate
import six


class OptOutDashboardView(BrowserView):
    """Personal dashboard for opt-out preferences"""

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.general_cookie_consent = None
        self.nextYear = DateTime() + 365
        request.set('disable_border', True)

    def __call__(self, *args, **kwargs):
        if 'form.submitted' in self.request.form:
            self._save_changes()
            api.portal.show_message(
                message=_(u'Changes saved'),
                type='info',
                request=self.request)
            self.request.response.redirect(
                '{0}/@@{1}'.format(
                    self.context.absolute_url(),
                    self.__name__)
                )
        return self.index()

    def _save_changes(self):
        request = self.request
        form = request.form
        if not form.get('accept_cookies'):
            # Cookie policy rejected: set all of the opt-out cookies
            optout_all(request, 'true', update=True)
            self.setOneYearCookie(config.COOKIECONSENT_NAME, 'false')
            return
        # Cookies consent given: let's save also opt-out cookies
        self.setOneYearCookie(config.COOKIECONSENT_NAME, 'true')
        for optout in self.settings().optout_configuration:
            value = 'true' if form.get('app_{0}'.format(optout.app_id)) == 'true' else 'false'  # noqa
            for cookie in optout.cookies:
                self.setOneYearCookie('{0}-optout'.format(cookie), value)

    def setOneYearCookie(self, name, value):
        setCookie(
            self.request.response,
            name,
            value,
            expires=self.nextYear.rfc822()
        )

    def _i18n_alternative(self, app_id, id):
        oo_i18n_id = u'{0}_optout_{1}'.format(app_id, id)
        oo_item = translate(_(oo_i18n_id), context=self.request)
        if six.text_type(oo_item) == oo_i18n_id:
            return app_id
        return oo_item

    @memoize
    def settings(self):
        registry = queryUtility(IRegistry)
        return registry.forInterface(ICookieConsentSettings, check=False)

    def optouts(self):
        settings = self.settings()
        request = self.request
        cookies = request.cookies
        portal_state = getMultiAdapter(
            (self.context, request), name=u'plone_portal_state')
        current_language = portal_state.language()
        self.general_cookie_consent = cookies.get(
            config.COOKIECONSENT_NAME, False) == 'true'

        results = []
        for oo_conf in settings.optout_configuration:
            optout = {}
            optout['id'] = oo_conf.app_id

            # i18n
            if len(oo_conf.texts) == 0:
                optout['title'] = self._i18n_alternative(
                    oo_conf.app_id, u'title')
                optout['description'] = self._i18n_alternative(
                    oo_conf.app_id, u'description')
            else:
                for i, app_text_content in enumerate(oo_conf.texts):
                    if current_language == app_text_content.lang:
                        optout['title'] = app_text_content.app_title if app_text_content.app_title else self._i18n_alternative(oo_conf.app_id, u'title')  # noqa
                        raw_i18n_desc = app_text_content.app_description if app_text_content.app_description else self._i18n_alternative(oo_conf.app_id, u'description')  # noqa
                        optout['description'] = '<br />'.join(raw_i18n_desc.strip().splitlines())  # noqa
                        break
                else:
                    # no lang found: use the first one as default
                    default_conf = oo_conf.texts[0]
                    optout['title'] = default_conf.app_title if default_conf.app_title else self._i18n_alternative(oo_conf.app_id, u'title')  # noqa
                    raw_i18n_desc = default_conf.app_description if default_conf.app_description else self._i18n_alternative(oo_conf.app_id, u'description')  # noqa
                    optout['description'] = '<br />'.join(raw_i18n_desc.strip().splitlines())  # noqa

            # check cookies: to enable the radio as "deny" we care about at
            # least of one cookie
            negative_cookies = [c for c in oo_conf.cookies
                    if not cookies.get("%s-optout" % c, None) or cookies["%s-optout" % c]=='false']  # noqa
            optout['cookie'] = False if negative_cookies else True
            results.append(optout)
        return results
