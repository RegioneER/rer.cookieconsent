# -*- coding: utf-8 -*-

from rer.cookieconsent import messageFactory as _
from zope import schema
from zope.interface import Interface
from zope.interface import implementer
from plone.registry.field import PersistentField
from z3c.form.object import registerFactoryAdapter
from zope.component.hooks import getSite


def default_language():
    site = getSite()
    return site.portal_languages.getDefaultLanguage().decode('utf-8')


class ICookieBannerEntry(Interface):
    """Single entry for the Cookie Consent banner configuration
    """

    lang = schema.Choice(
        title=_(u"Language"),
        defaultFactory=default_language,
        missing_value=u"",
        required=True,
        vocabulary=u"rer.cookieconsent.vocabularies.AvailableLanguages"
    )

    text = schema.Text(
        title=_(u"Cookie consent warning text"),
        description=_('text_help',
                      default=u"Provide the text to be put inside the cookie consent banner.\n"
                              u"You can (must) use HTML here but you can still avoit it.\n"
                              u"Use the \"$privacy_link\" marker to insert an HTML link to the privacy policy (see below).\n"
                              u"If you want full controls over the HTML generated you can use the \"$privacy_link_url\" marker"
                              u"(URL of the link) and \"$privacy_link_text\" (text of the link)."),
        default=u"",
        missing_value=u"",
        required=True,
    )

    privacy_link_url = schema.TextLine(
        title=_(u'URL of the privacy Policy'),
        description=_('privacy_link_url_help',
                      default=u"An URL, or a absolute path, to a page where user can see the full "
                              u"provacy policy of your site.\n"
                              u"Examples: \"http://externalsite.com/privacy.html\", \"/internal/document\"."),
        required=False,
    )

    privacy_link_text = schema.TextLine(
        title=_(u'Text of the privacy Policy'),
        description=_('privacy_link_text_help',
                      default=u"The text to be used when generating the URL specified in the "
                              u"\"URL of the privacy Policy\".\n"
                              u"If not provided, the full URL is used."),
        required=False,
    )


class IOptOutEntry(Interface):
    """Single entry for an Opt-Out application configuration 
    """

    app_id = schema.ASCIILine(
        title=_(u'Application id'),
        description=_('app_id_help',
                      default=u"A unique id for the opt-out group"),
        default="",
        missing_value="",
        required=True,
    )

    cookies = schema.Tuple(
        title=_(u'Cookies'),
        description=_('cookies_help',
                      default=u"A list of cookies names prefixes.\n"
                      u"This opt-out will generate a cookie in the form PREFIX-optout for every defined prefix"),
        required=True,
        value_type=schema.ASCIILine(),
    )

    app_title = schema.TextLine(
        title=_(u'Application title'),
        description=_('app_title_help',
                      default=u"This will be the title used in the opt-out configuration dashboard.\n"
                              u"If not provided, a translation for \"APP_ID_optout_title\" will be used"),
        default=u"",
        missing_value=u"",
        required=False,
    )

    app_description = schema.Text(
        title=_(u'Application description'),
        description=_('app_description_help',
                      default=u"A long description that must explain what this opt-out will do if activated.\n"
                              u"If not provided, a translation for \"APP_ID_optout_description\" will be used"),
        default=u"",
        missing_value=u"",
        required=False,
    )


@implementer(ICookieBannerEntry)
class CookieBannerEntry(object):

    def __init__(self, lang=u'', text=u'', privacy_link_url=u'', privacy_link_text=u''):
        self.lang = lang
        self.text = text
        self.privacy_link_url = privacy_link_url
        self.privacy_link_text = privacy_link_text


@implementer(IOptOutEntry)
class OptOutEntry(object):

    def __init__(self, app_id=u'', cookies=[], app_title=u'', app_description=u''):
        self.app_id = app_id
        self.cookies = cookies
        self.app_title = app_title
        self.app_description = app_description


class ICookieBannerEntryPersistentObject(Interface):
    pass

@implementer(ICookieBannerEntryPersistentObject)
class CookieBannerEntryPersistentObject(PersistentField, schema.Object):
    pass


class IOptOutEntryPersistentObject(Interface):
    pass

@implementer(IOptOutEntryPersistentObject)
class OptOutEntryPersistentObject(PersistentField, schema.Object):
    pass



class ICookieBannerSettings(Interface):
    """Settings for the Cookie Consent banner
    """

    accept_on_click = schema.Bool(
            title=_(u'Accept policy on every click'),
            description=_('help_accept_on_click',
                          default=u"If checked, any click on links on any page will be interpreted as the "
                                  u"user accepted the cookie policy (like if they explicitly accepted it)."),
            required=False,
            default=False,
    )

    cookie_consent_configuration = schema.Tuple(
            title=_(u'Cookie consent configuration'),
            description=_('help_cookie_consent_configuration',
                          default=u"For every involved language in the site, provide a configuration of the cookie "
                                  u"consent banner.\n"
                                  u"The first defined policy configuration will be the default ones "
                                  u"(the ones used when not language specific configuration is found)"),
            value_type=CookieBannerEntryPersistentObject(ICookieBannerEntry, title=_(u"Cookie consent banner configuration")),
            required=False,
            default=(),
            missing_value=(),
    )


class IOptOutSettings(Interface):
    """Settings for the Optout"""

    optout_configuration = schema.Tuple(
            title=_(u'Opt-out configurations'),
            description=_('help_optout_configuration',
                          default=u"When the user accepted the general privacy policy he can still accept/decline "
                                  u"a single kind of cookie(s) from a 3rd part application.\n"
                                  u"From this panel you can configure opt-out cookies for those applications.\n"
                                  u"PLEASE NOTE: this product will only handle and generate cookies, is duty of "
                                  u"others products to use those cookies in the correct manner."),
            value_type=OptOutEntryPersistentObject(IOptOutEntry, title=_(u"Opt-out configuration")),
            required=False,
            default=(),
            missing_value=(),
    )




class ICookieConsentSettings(ICookieBannerSettings, IOptOutSettings):
    """Settings used in the control panel for cookiecosent: unified panel
    """


registerFactoryAdapter(ICookieBannerEntry, CookieBannerEntry)
registerFactoryAdapter(IOptOutEntry, OptOutEntry)

