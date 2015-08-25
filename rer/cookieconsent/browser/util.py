# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from rer.cookieconsent.init_cookies import optout_all


class ResetOptoutView(BrowserView):
    """Set all of the opt-out cookies to false"""

    def __call__(self, *args, **kwargs):
        optout_all(self.request, 'false', update=True)
        back_to = self.request.form.get('came_from') or self.context.absolute_url()
        self.request.response.redirect(back_to)
