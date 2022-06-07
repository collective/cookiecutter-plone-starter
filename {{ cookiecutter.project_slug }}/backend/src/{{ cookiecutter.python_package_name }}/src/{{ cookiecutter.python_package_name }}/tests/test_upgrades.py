"""Upgrades tests for this package."""
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from {{ cookiecutter.python_package_name }}.testing import {{ cookiecutter.__python_package_name_upper }}_INTEGRATION_TESTING  # noqa: E501
from Products.GenericSetup.upgrade import listUpgradeSteps

import unittest


class UpgradeStepIntegrationTest(unittest.TestCase):

    layer = {{ cookiecutter.__python_package_name_upper }}_INTEGRATION_TESTING
    profile = "{{ cookiecutter.python_package_name }}:default"
    src = ""
    dst = ""
    steps = 1

    def setUp(self):
        self.portal = self.layer["portal"]
        self.setup = self.portal["portal_setup"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def _match(self, item, source, dest):
        source, dest = tuple([source]), tuple([dest])
        return item["source"] == source and item["dest"] == dest

    def available_steps(self) -> list:
        """Test available steps."""
        steps = listUpgradeSteps(self.setup, self.profile, self.src)
        steps = [s for s in steps if self._match(s[0], self.src, self.dst)]
        return steps

    def test_available(self):
        """Test upgrade step is available."""
        if self.src and self.dst:
            steps = self.available_steps()
            self.assertEqual(len(steps), 1)

# Example of upgrade step test
# class V{{ cookiecutter.__profile_version }}UpgradeTest(UpgradeStepIntegrationTest):
#     """Test upgrade step from version {{ cookiecutter.__profile_version }}."""

#     src = "{{ cookiecutter.__profile_version }}"
#     dst = "20230229001"
#     steps = 1
