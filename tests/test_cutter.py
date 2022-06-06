"""Test cookiecutter generation."""
import re
from pathlib import Path
from typing import List

import pytest

PATTERN = "{{( ?cookiecutter)[.](.*?)}}"
RE_OBJ = re.compile(PATTERN)


def build_files_list(root_dir: Path) -> List[Path]:
    """Build a list containing absolute paths to the generated files."""
    return [path for path in Path(root_dir).glob("*") if path.is_file()]


def test_default_configuration(cookies, context: dict):
    """Generated project should replace all variables."""
    result = cookies.bake(extra_context=context)
    assert result.exception is None
    assert result.exit_code == 0
    assert result.project_path.name == context["project_slug"]
    assert result.project_path.is_dir()


def test_variable_substitution(cutter_result):
    """Check if no file was unprocessed."""
    paths = build_files_list(cutter_result.project_path)
    for path in paths:
        for line in open(path, "r"):
            match = RE_OBJ.search(line)
            msg = f"cookiecutter variable not replaced in {path}"
            assert match is None, msg


FOLDERS = [
    ".github",
    "backend",
    "devops",
    "frontend",
]


@pytest.mark.parametrize("folder_name", FOLDERS)
def test_root_folders(cutter_result, folder_name: str):
    """Test folders were created."""
    folder = cutter_result.project_path / folder_name
    assert folder.is_dir()


FILES = [
    "CHANGELOG.md",
    "Makefile",
    "README.md",
]


@pytest.mark.parametrize("file_name", FILES)
def test_root_files(cutter_result, file_name: str):
    """Test files were created."""
    path = cutter_result.project_path / file_name
    assert path.is_file()
