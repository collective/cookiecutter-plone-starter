"""Pytest configuration."""

import pytest


@pytest.fixture(scope="session")
def context() -> dict:
    """Cookiecutter context."""
    return {
        "project_title": "Plone Brasil",
        "project_slug": "plone.org.br",
        "description": "Brazilian community website.",
        "author": "PloneGov-BR",
        "email": "gov@plone.org.br",
        "python_package_name": "ploneorgbr",
        "volto_addon_name": "volto-ploneorgbr",
        "python_test_framework": "pytest",
        "plone_version": "6.0.0a4",
        "volto_version": "16.0.0-alpha.4",
        "language_code": "en",
        "github_organization": "plonegovbr",
        "container_registry": "GitHub",
    }


@pytest.fixture(scope="session")
def context_unittest() -> dict:
    """Cookiecutter context."""
    return {
        "project_title": "Plone Brasil",
        "project_slug": "plone.org.br",
        "description": "Brazilian community website.",
        "author": "PloneGov-BR",
        "email": "gov@plone.org.br",
        "python_package_name": "ploneorgbr",
        "volto_addon_name": "volto-ploneorgbr",
        "python_test_framework": "unittest",
        "plone_version": "6.0.0a4",
        "volto_version": "16.0.0-alpha.4",
        "language_code": "en",
        "github_organization": "plonegovbr",
        "container_registry": "GitHub",
    }


@pytest.fixture(scope="session")
def bad_context() -> dict:
    """Cookiecutter context with invalid data."""
    return {
        "project_title": "Plone Brasil",
        "project_slug": "plone.org.br",
        "description": "Brazilian community website.",
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
