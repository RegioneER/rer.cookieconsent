# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from rer.cookieconsent.init_cookies import optout_all
from zope.publisher.interfaces.browser import IBrowserView


class ResetOptoutView(BrowserView):
    """Set all of the opt-out cookies to false
    Redirect to "current" page after that.
    """

    def __call__(self, *args, **kwargs):
        optout_all(self.request, 'false', update=True)
        context = self.context
        if IBrowserView.providedBy(context):
            # This context is also a view, we called something like
            # /foo/bar/@@view/@@reset-optout
            here_url = '{0}/@@{1}'.format(
                context.context.absolute_url(),
                context.__name__)
        else:
            here_url = context.absolute_url()
        came_from = self.request.form.get('came_from')
        if came_from and getToolByName(self.context, 'portal_url').isURLInPortal(came_from):
            back_to = came_from
        else:
            back_to = here_url
        self.request.response.redirect(back_to)
