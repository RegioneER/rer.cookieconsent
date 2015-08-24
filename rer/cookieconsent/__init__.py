# -*- extra stuff goes here -*-

import logging

from zope.i18nmessageid import MessageFactory

messageFactory = MessageFactory('rer.cookieconsent')
logger = logging.getLogger('rer.cookieconsent')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
