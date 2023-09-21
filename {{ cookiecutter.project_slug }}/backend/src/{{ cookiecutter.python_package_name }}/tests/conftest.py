from {{ cookiecutter.python_package_name }}.testing import INTEGRATION_TESTING
from pytest_plone import fixtures_factory


pytest_plugins = ["pytest_plone"]


globals().update(fixtures_factory(((INTEGRATION_TESTING, "integration"),)))
