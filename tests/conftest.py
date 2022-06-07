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
        "volto_version": "v16.0.0-alpha.4",
        "language_code": "en",
        "github_organization": "plonegovbr",
    }


@pytest.fixture(scope="session")
def cutter_result(cookies_session, context):
    """Cookiecutter result."""
    return cookies_session.bake(extra_context=context)
