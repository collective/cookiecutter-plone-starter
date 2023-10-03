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
    ".dockerignore",
    ".editorconfig",
    ".eslintignore",
    ".eslintrc.js",
    ".gitignore",
    ".prettierignore",
    ".yarnrc.yml",
    "babel.config.js",
    "cypress.config.js",
    "mrs.developer.json",
    "package.json",
    "package.json.tpl",
    "razzle.config.js",
    "README.md",
    "yarn.lock",
]


@pytest.mark.parametrize("filename", EXPECTED_FILES)
def test_frontend_files(cutter_result, filename: str):
    """Test @plone/volto generator files exist."""
    frontend_folder = cutter_result.project_path / "frontend"
    path = frontend_folder / filename
    assert path.is_file()


def test_frontend_config_json(cutter_result):
    """Test frontend has either jsconfig.json or tsconfig.json."""
    frontend_folder = cutter_result.project_path / "frontend"
    js_path = frontend_folder / "jsconfig.json"
    ts_path = frontend_folder / "tsconfig.json"
    assert js_path.is_file() or ts_path.is_file()
