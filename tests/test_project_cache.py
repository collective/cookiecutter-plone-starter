"""Test Generator: /varnish (And Cache support)."""
import pytest


CACHE_FILES = [
    "backend/src/ploneorgbr/src/ploneorgbr/profiles/default/registry/plone.cachepurging.interfaces.ICachePurgingSettings.xml",
    "backend/src/ploneorgbr/src/ploneorgbr/profiles/default/registry/plone.caching.interfaces.ICacheSettings.xml",
    "varnish/Dockerfile",
    "varnish/etc/varnish.vcl",
]

GHA_ACTIONS_CI = [
    ".github/workflows/varnish.yml",
]


DEVOPS_FILES = CACHE_FILES + GHA_ACTIONS_CI


@pytest.mark.parametrize("filepath", DEVOPS_FILES)
def test_project_cache_files(cutter_devops_result_cache, filepath: str):
    """Test created files."""
    folder = cutter_devops_result_cache.project_path
    path = folder / filepath
    assert path.is_file()


@pytest.mark.parametrize("filepath", CACHE_FILES)
def test_project_no_cache(cutter_result_devops_no_cache, filepath: str):
    """Test Cache-related files are not present."""
    folder = cutter_result_devops_no_cache.project_path
    path = folder / filepath
    assert path.exists() is False
