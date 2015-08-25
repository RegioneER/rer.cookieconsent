# -*- coding: utf-8 -*-

#from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from rer.cookieconsent import messageFactory as _
from rer.cookieconsent.controlpanel.interfaces import ICookieConsentSettings
from rer.cookieconsent.controlpanel.interfaces import ICookieBannerSettings
from rer.cookieconsent.controlpanel.interfaces import IOptOutSettings
from plone.app.registry.browser import controlpanel
from Products.CMFPlone import PloneMessageFactory as pmf
from z3c.form import button
from z3c.form import field
from z3c.form import group


def fix_widget_style(widget):
    widget.style = u'width: 100%';
    widget.klass += u" autoresize";
    widget.rows = 7


class FormCookieConsentBanner(group.Group):
    label = _(u"Cookie consent banner")
    fields = field.Fields(ICookieBannerSettings)


class FormOptOut(group.Group):
    label = _(u"Opt-out dashboard")
    fields = field.Fields(IOptOutSettings)


class CookieConsentSettingsEditForm(controlpanel.RegistryEditForm):
    """Media settings form.
    """
    schema = ICookieConsentSettings
    #fields = field.Fields(ICookieBannerSettings)
    groups = (FormCookieConsentBanner, FormOptOut)
    id = "CookieConsentSettingsEditForm"
    label = _(u"Cookie consent configuration")
    description = _(u"Configuration of the cookie consent product")

    @button.buttonAndHandler(pmf('Save'), name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(_(u"Changes saved"),
                                                      "info")
        self.context.REQUEST.RESPONSE.redirect("@@%s" % self.__name__)

    @button.buttonAndHandler(pmf('Cancel'), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_(u"Changes cancelled"),
                                                      "info")
        self.request.response.redirect("%s/%s" % (self.context.absolute_url(),
                                                  self.control_panel_view))

#    def updateWidgets(self):
#        super(CookieConsentSettingsEditForm, self).updateWidgets()
#        for main_widget in self.widgets['cookie_consent_configuration'].widgets:
#        for main_widget in self.groups[0].fields['cookie_consent_configuration'].widgets:
#            widgets = main_widget.subform.widgets
#            fix_widget_style(error_widgets['text'])
#            widgets['privacy_link_url'].style = u'width: 100%'
#            widgets['privacy_link_text'].style = u'width: 100%'


class CookieConsentSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    """Analytics settings control panel.
    """
    form = CookieConsentSettingsEditForm
    #index = ViewPageTemplateFile('controlpanel.pt')

