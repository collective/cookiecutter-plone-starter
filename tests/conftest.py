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
        "plone_version": "6.0.0a4",
        "volto_version": "16.0.0-alpha.4",
        "language_code": "en",
        "github_organization": "plonegovbr",
        "container_registry": "Docker Hub",
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
