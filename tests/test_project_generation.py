"""Test Generator: /."""
import json

import pytest
import yaml


@pytest.mark.parametrize(
    "filepath",
    [
        ".editorconfig",
        ".gitignore",
        ".vscode/settings.json",
        "CHANGELOG.md",
        "Makefile",
        "README.md",
        "version.txt",
    ],
)
def test_project_files(cutter_result, filepath: str):
    """Test created files."""
    folder = cutter_result.project_path
    path = folder / filepath
    assert path.is_file()


@pytest.mark.parametrize(
    "filepath",
    [
        "frontend/mrs.developer.json",
        "frontend/package.json",
        "frontend/tsconfig.json",
        "frontend/cypress/fixtures/example.json",
        "frontend/src/addons/volto-ploneorgbr/.release-it.json",
        "frontend/src/addons/volto-ploneorgbr/package.json",
        "frontend/src/addons/volto-ploneorgbr/acceptance/package.json",
        "frontend/src/addons/volto-ploneorgbr/acceptance/cypress/fixtures/example.json",
        ".vscode/settings.json",
    ],
)
def test_valid_json_files(cutter_result, filepath: str):
    """Test generated json files are valid."""
    folder = cutter_result.project_path
    path = folder / filepath
    with open(path, "r") as fh:
        content = json.load(fh)
    assert content
