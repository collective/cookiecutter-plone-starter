"""Pytest configuration."""
from copy import deepcopy

import pytest

PLONE_VERSION = "6.0.7"
VOLTO_VERSION = "17.0.0"
GENERATOR_VERSION = "7.0.1"


@pytest.fixture(scope="session")
def context() -> dict:
    """Cookiecutter context."""
    return {
        "project_title": "Plone Brasil",
        "project_slug": "plone.org.br",
        "description": "Brazilian community website.",
        "hostname": "plone.org.br",
        "author": "PloneGov-BR",
        "email": "gov@plone.org.br",
        "python_package_name": "ploneorgbr",
        "volto_addon_name": "volto-ploneorgbr",
        "python_test_framework": "pytest",
        "plone_version": PLONE_VERSION,
        "volto_version": VOLTO_VERSION,
        "volto_generator_version": GENERATOR_VERSION,
        "language_code": "en",
        "github_organization": "plonegovbr",
        "container_registry": "GitHub",
    }


@pytest.fixture(scope="session")
def context_unittest(context) -> dict:
    """Cookiecutter context."""
    new_context = deepcopy(context)
    new_context["python_test_framework"] = "unittest"
    return new_context


@pytest.fixture(scope="session")
def context_devops_no_ansible(context) -> dict:
    """Cookiecutter context."""
    new_context = deepcopy(context)
    new_context["devops_ansible"] = "0"
    return new_context


@pytest.fixture(scope="session")
def context_devops_no_gha_deploy(context) -> dict:
    """Cookiecutter context."""
    new_context = deepcopy(context)
    new_context["devops_gha_deploy"] = "0"
    return new_context


@pytest.fixture(scope="session")
def bad_context() -> dict:
    """Cookiecutter context with invalid data."""
    return {
        "project_title": "Plone Brasil",
        "project_slug": "plone.org.br",
        "description": "Brazilian community website.",
        "hostname": "https://plone.org.br",  # error
        "author": "PloneGov-BR",
        "email": "gov@plone.org.br",
        "python_package_name": "plone-org-br",  # error
        "volto_addon_name": "volto-ploneorgbr",
        "plone_version": "5.2.8",  # error
        "volto_version": "16.0.0-alpha.4",
        "language_code": "en-",  # error
        "github_organization": "plonegovbr",
        "container_registry": " ",  # error
    }


@pytest.fixture(scope="session")
def cutter_result(cookies_session, context):
    """Cookiecutter result."""
    return cookies_session.bake(extra_context=context)


@pytest.fixture(scope="session")
def cutter_result_unittest(cookies_session, context_unittest):
    """Cookiecutter result."""
    return cookies_session.bake(extra_context=context_unittest)


@pytest.fixture(scope="session")
def cutter_result_devops_no_ansible(cookies_session, context_devops_no_ansible):
    """Cookiecutter result."""
    return cookies_session.bake(extra_context=context_devops_no_ansible)


@pytest.fixture(scope="session")
def cutter_result_devops_no_gha_deploy(cookies_session, context_devops_no_gha_deploy):
    """Cookiecutter result."""
    return cookies_session.bake(extra_context=context_devops_no_gha_deploy)
