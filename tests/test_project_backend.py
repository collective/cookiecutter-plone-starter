"""Test Generator: /backend."""

import pytest

BACKEND_FILES = [
    ".dockerignore",
    ".gitattributes",
    ".gitignore",
    "Dockerfile.acceptance",
    "Dockerfile",
    "instance.yaml",
    "Makefile",
    "mx.ini",
    "pyproject.toml",
    "requirements-docker.txt",
    "requirements.txt",
    "version.txt",
]


@pytest.mark.parametrize("filename", BACKEND_FILES)
def test_backend_top_level_files(cutter_result, filename: str):
    """Test backend files."""
    backend_folder = cutter_result.project_path / "backend"
    path = backend_folder / filename
    assert path.is_file()


BACKEND_PACKAGE_FILES_PYTEST = [
    "src/ploneorgbr/setup.py",
    "src/ploneorgbr/src/ploneorgbr/configure.zcml",
    "src/ploneorgbr/src/ploneorgbr/dependencies.zcml",
    "src/ploneorgbr/src/ploneorgbr/permissions.zcml",
    "src/ploneorgbr/src/ploneorgbr/profiles.zcml",
    "src/ploneorgbr/src/ploneorgbr/testing.py",
    "src/ploneorgbr/tests/conftest.py",
    "src/ploneorgbr/tests/setup/test_setup_install.py",
    "src/ploneorgbr/tests/setup/test_setup_uninstall.py",
]


@pytest.mark.parametrize("filename", BACKEND_FILES)
def test_backend_package_files_pytest(cutter_result, filename: str):
    """Test backend files."""
    backend_folder = cutter_result.project_path / "backend"
    path = backend_folder / filename
    assert path.is_file()


BACKEND_PACKAGE_FILES_PYTEST = [
    "src/ploneorgbr/setup.py",
    "src/ploneorgbr/src/ploneorgbr/configure.zcml",
    "src/ploneorgbr/src/ploneorgbr/dependencies.zcml",
    "src/ploneorgbr/src/ploneorgbr/permissions.zcml",
    "src/ploneorgbr/src/ploneorgbr/profiles.zcml",
    "src/ploneorgbr/src/ploneorgbr/testing.py",
    "src/ploneorgbr/src/ploneorgbr/tests/__init__.py",
    "src/ploneorgbr/src/ploneorgbr/tests/test_setup.py",
]


@pytest.mark.parametrize("filename", BACKEND_FILES)
def test_backend_package_files_unittest(cutter_result_unittest, filename: str):
    """Test backend package files."""
    backend_folder = cutter_result_unittest.project_path / "backend"
    path = backend_folder / filename
    assert path.is_file()
