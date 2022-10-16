"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from {{ cookiecutter.python_package_name }}.testing import {{ cookiecutter.__python_package_name_upper }}_INTEGRATION_TESTING  # noqa: E501
from Products.CMFPlone.utils import get_installer

import unittest


class TestSetup(unittest.TestCase):
    """Test that {{ cookiecutter.python_package_name }} is properly installed."""

    layer = {{ cookiecutter.__python_package_name_upper }}_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.setup = self.portal.portal_setup
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if {{ cookiecutter.python_package_name }} is installed."""
        self.assertTrue(self.installer.is_product_installed("{{ cookiecutter.python_package_name }}"))

    def test_browserlayer(self):
        """Test that I{{ cookiecutter.__python_package_name_upper }}Layer is registered."""
        from plone.browserlayer import utils
        from {{ cookiecutter.python_package_name }}.interfaces import I{{ cookiecutter.__python_package_name_upper }}Layer

        self.assertIn(I{{ cookiecutter.__python_package_name_upper }}Layer, utils.registered_layers())

    def test_latest_version(self):
        """Test latest version of default profile."""
        self.assertEqual(
            self.setup.getLastVersionForProfile("{{ cookiecutter.python_package_name }}:default")[0],
            "{{ cookiecutter.__profile_version }}",
        )


class TestUninstall(unittest.TestCase):

    layer = {{ cookiecutter.__python_package_name_upper }}_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("{{ cookiecutter.python_package_name }}")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if {{ cookiecutter.python_package_name }} is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("{{ cookiecutter.python_package_name }}"))

    def test_browserlayer_removed(self):
        """Test that I{{ cookiecutter.__python_package_name_upper }}Layer is removed."""
        from plone.browserlayer import utils
        from {{ cookiecutter.python_package_name }}.interfaces import I{{ cookiecutter.__python_package_name_upper }}Layer

        self.assertNotIn(I{{ cookiecutter.__python_package_name_upper }}Layer, utils.registered_layers())
