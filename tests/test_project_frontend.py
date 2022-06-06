"""Test Generator: /frontend."""
import pytest

FRONTEND_FILES = [
    ".dockerignore",
    "Dockerfile",
    "Makefile",
]


@pytest.mark.parametrize("filename", FRONTEND_FILES)
def test_frontend_files(cutter_result, filename: str):
    """Test frontend files."""
    frontend_folder = cutter_result.project_path / "frontend"
    path = frontend_folder / filename
    assert path.is_file()
