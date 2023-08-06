# -*- coding: utf-8 -*-
# from plone.app.textfield import RichText
# from plone.autoform import directives
from plone.dexterity.content import Container

# from plone.namedfile import field as namedfile
from plone.supermodel import model

# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
# from zope import schema
from zope.interface import implementer


# from derico.article import _


class IArticlePage(model.Schema):
    """
    """


@implementer(IArticlePage)
class ArticlePage(Container):
    """Content-type class for IArticlePage"""
