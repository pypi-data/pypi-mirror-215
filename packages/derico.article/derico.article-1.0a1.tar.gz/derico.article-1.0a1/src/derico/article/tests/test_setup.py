# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from derico.article.testing import DERICO_ARTICLE_INTEGRATION_TESTING  # noqa: E501
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that derico.article is properly installed."""

    layer = DERICO_ARTICLE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")

    def test_product_installed(self):
        """Test if derico.article is installed."""
        self.assertTrue(self.installer.is_product_installed("derico.article"))

    def test_browserlayer(self):
        """Test that IDericoArticleLayer is registered."""
        from derico.article.interfaces import IDericoArticleLayer
        from plone.browserlayer import utils

        self.assertIn(IDericoArticleLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = DERICO_ARTICLE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("derico.article")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if derico.article is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("derico.article"))

    def test_browserlayer_removed(self):
        """Test that IDericoArticleLayer is removed."""
        from derico.article.interfaces import IDericoArticleLayer
        from plone.browserlayer import utils

        self.assertNotIn(IDericoArticleLayer, utils.registered_layers())
