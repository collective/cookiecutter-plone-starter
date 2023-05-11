from {{ cookiecutter.python_package_name }} import PACKAGE_NAME

import pytest


class TestSetupUninstall:
    @pytest.fixture(autouse=True)
    def uninstalled(self, installer):
        installer.uninstall_product(PACKAGE_NAME)

    def test_product_uninstalled(self, installer):
        """Test if {{ cookiecutter.python_package_name }} is cleanly uninstalled."""
        assert installer.is_product_installed(PACKAGE_NAME) is False

    def test_browserlayer_removed(self, browser_layers):
        """Test that ICaseStudyLayer is removed."""
        from {{ cookiecutter.python_package_name }}.interfaces import I{{ cookiecutter.__python_package_name_upper }}Layer

        assert I{{ cookiecutter.__python_package_name_upper }}Layer not in browser_layers
