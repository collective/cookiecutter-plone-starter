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
    "pyproject.toml",
    "requirements.txt",
]


@pytest.mark.parametrize("filename", BACKEND_FILES)
def test_backend_files(cutter_result, filename: str):
    """Test backend files."""
    backend_folder = cutter_result.project_path / "backend"
    path = backend_folder / filename
    assert path.is_file()
