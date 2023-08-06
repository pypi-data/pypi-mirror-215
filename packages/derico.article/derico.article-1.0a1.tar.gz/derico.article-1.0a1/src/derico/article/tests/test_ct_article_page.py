# -*- coding: utf-8 -*-
from derico.article.content.article_page import IArticlePage  # NOQA E501
from derico.article.testing import DERICO_ARTICLE_INTEGRATION_TESTING  # noqa
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class ArticlePageIntegrationTest(unittest.TestCase):

    layer = DERICO_ARTICLE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.parent = self.portal

    def test_ct_article_page_schema(self):
        fti = queryUtility(IDexterityFTI, name="ArticlePage")
        schema = fti.lookupSchema()
        self.assertEqual(IArticlePage, schema)

    def test_ct_article_page_fti(self):
        fti = queryUtility(IDexterityFTI, name="ArticlePage")
        self.assertTrue(fti)

    def test_ct_article_page_factory(self):
        fti = queryUtility(IDexterityFTI, name="ArticlePage")
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IArticlePage.providedBy(obj),
            "IArticlePage not provided by {0}!".format(
                obj,
            ),
        )

    def test_ct_article_page_adding(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        obj = api.content.create(
            container=self.portal,
            type="ArticlePage",
            id="article_page",
        )

        self.assertTrue(
            IArticlePage.providedBy(obj),
            "IArticlePage not provided by {0}!".format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn("article_page", parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn("article_page", parent.objectIds())

    def test_ct_article_page_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        fti = queryUtility(IDexterityFTI, name="ArticlePage")
        self.assertTrue(fti.global_allow, "{0} is not globally addable!".format(fti.id))

    def test_ct_article_page_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        fti = queryUtility(IDexterityFTI, name="ArticlePage")
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            "article_page_id",
            title="ArticlePage container",
        )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type="Document",
                title="My Content",
            )
