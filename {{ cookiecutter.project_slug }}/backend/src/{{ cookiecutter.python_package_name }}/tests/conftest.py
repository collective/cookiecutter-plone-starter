from {{ cookiecutter.python_package_name }}.testing import {{ cookiecutter.__python_package_name_upper }}_INTEGRATION_TESTING
from pytest_plone import fixtures_factory


pytest_plugins = ["pytest_plone"]


globals().update(fixtures_factory((({{ cookiecutter.__python_package_name_upper }}_INTEGRATION_TESTING, "integration"),)))
