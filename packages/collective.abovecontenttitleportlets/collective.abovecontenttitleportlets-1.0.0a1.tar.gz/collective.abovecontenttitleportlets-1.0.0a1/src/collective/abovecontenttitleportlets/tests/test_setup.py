"""Setup tests for this package."""
from collective.abovecontenttitleportlets.testing import (
    COLLECTIVE_ABOVE_CONTENT_PORTLETS_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.portlets.interfaces import IPortletManager
from zope.component import getSiteManager

import unittest


try:
    from plone.base.utils import get_installer
except ImportError:
    from Products.CMFPlone.utils import get_installer


class TestSetup(unittest.TestCase):
    """Test that collective.abovecontenttitleportlets is properly installed."""

    layer = COLLECTIVE_ABOVE_CONTENT_PORTLETS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if collective.abovecontenttitleportlets is installed."""
        self.assertTrue(
            self.installer.is_product_installed("collective.abovecontenttitleportlets")
        )

    def test_browserlayer(self):
        """Test that ICollectiveAboveContentTitlePortletsLayer is registered."""
        from collective.abovecontenttitleportlets.interfaces import (
            ICollectiveAboveContentTitlePortletsLayer,
        )
        from plone.browserlayer import utils

        self.assertIn(
            ICollectiveAboveContentTitlePortletsLayer, utils.registered_layers()
        )

    def test_portlet_manager_registered(self):
        sm = getSiteManager(self.portal)
        registrations = [
            r.name for r in sm.registeredUtilities() if IPortletManager == r.provided
        ]
        self.assertIn("collective.abovecontenttitleportlets", registrations)


class TestUninstall(unittest.TestCase):
    layer = COLLECTIVE_ABOVE_CONTENT_PORTLETS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("collective.abovecontenttitleportlets")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.abovecontenttitleportlets is cleanly uninstalled."""
        self.assertFalse(
            self.installer.is_product_installed("collective.abovecontenttitleportlets")
        )

    def test_browserlayer_removed(self):
        """Test that ICollectiveAboveContentTitlePortletsLayer is removed."""
        from collective.abovecontenttitleportlets.interfaces import (
            ICollectiveAboveContentTitlePortletsLayer,
        )
        from plone.browserlayer import utils

        self.assertNotIn(
            ICollectiveAboveContentTitlePortletsLayer, utils.registered_layers()
        )

    def test_portlet_manager_removed(self):
        sm = getSiteManager(self.portal)
        registrations = [
            r.name for r in sm.registeredUtilities() if IPortletManager == r.provided
        ]
        self.assertNotIn("collective.abovecontenttitleportlets", registrations)
