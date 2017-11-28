# -*- coding: utf-8 -*-
from zope.i18nmessageid import MessageFactory

import logging


messageFactory = MessageFactory('rer.cookieconsent')
logger = logging.getLogger('rer.cookieconsent')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
