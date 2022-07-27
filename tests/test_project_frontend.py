"""Test Generator: /frontend."""
import pytest

RENAMED_FILES = [
    ".dockerignore",
    "Dockerfile",
    "Makefile",
]


@pytest.mark.parametrize("filename", RENAMED_FILES)
def test_renamed_files(cutter_result, filename: str):
    """Test template files were renamed."""
    frontend_folder = cutter_result.project_path / "frontend"
    path = frontend_folder / filename
    assert path.is_file()


EXPECTED_FILES = [
    "jsconfig.json",
    "mrs.developer.json",
    "package.json",
    "README.md",
    "yarn.lock",
]


@pytest.mark.parametrize("filename", EXPECTED_FILES)
def test_frontend_files(cutter_result, filename: str):
    """Test @plone/volto generator files exist."""
    frontend_folder = cutter_result.project_path / "frontend"
    path = frontend_folder / filename
    assert path.is_file()
