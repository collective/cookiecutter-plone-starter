import re

import requests
from cookiecutter.utils import simple_filter

REGISTRIES = {
    "Docker Hub": "",
    "GitHub": "ghcr.io/",
}


VOLTO_MIN_VERSION = 16
VOLTO_GENERATOR_MIN_VERSION = 6


@simple_filter
def latest_volto(v) -> str:
    """Return the latest volto version."""
    url: str = "https://registry.npmjs.org/@plone/volto"
    resp = requests.get(url, headers={"Accept": "application/vnd.npm.install-v1+json"})
    data = resp.json()
    versions = [version for version in data["dist-tags"].values()]
    valid_versions = [v for v in versions if int(v.split(".")[0]) >= VOLTO_MIN_VERSION]
    return valid_versions[0]


@simple_filter
def latest_volto_generator(v) -> str:
    """Return the latest volto generator version."""
    url: str = "https://registry.npmjs.org/@plone/generator-volto"
    resp = requests.get(url, headers={"Accept": "application/vnd.npm.install-v1+json"})
    data = resp.json()
    versions = [version for version in data["dist-tags"].values()]
    valid_versions = [
        v for v in versions if int(v.split(".")[0]) >= VOLTO_GENERATOR_MIN_VERSION
    ]
    return valid_versions[0]


@simple_filter
def latest_plone(v) -> str:
    """Return the latest plone version."""
    url: str = "https://dist.plone.org/release/6.0-latest/constraints.txt"
    resp = requests.get(url)
    data = resp.content.decode("utf-8")
    return re.search("\nPlone==(.*)\n", data).groups()[0]


@simple_filter
def gs_language_code(code: str) -> str:
    """Return the language code as expected by Generic Setup."""
    gs_code = code.lower()
    if "-" in code:
        base_language, country = code.split("-")
        gs_code = f"{base_language}-{country.lower()}"
    return gs_code


@simple_filter
def docker_image_prefix(registry: str) -> str:
    """Return the a prefix to be used with all Docker images."""
    return REGISTRIES.get(registry, "")
