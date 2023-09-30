import os
import re

import requests
from cookiecutter.utils import simple_filter

REGISTRIES = {
    "Docker Hub": "",
    "GitHub": "ghcr.io/",
}


VOLTO_MIN_VERSION = 16
VOLTO_GENERATOR_MIN_VERSION = 6

DEFAULT_NODE = "18"

VOLTO_NODE = {
    16: 16,
    17: DEFAULT_NODE,
}


def latest_version(versions, min_version, include_alphas=False):
    valid = sorted(
        [v for v in versions if int(v.split(".")[0]) >= min_version], reverse=True
    )
    if not include_alphas:
        valid = [v for v in valid if "-" not in v]
    return valid[0]


@simple_filter
def use_alpha_versions(v: str) -> str:
    """Should we use alpha versions of Volto."""
    use_alpha_versions = "Yes" if "USE_VOLTO_ALPHA" in os.environ else "No"
    return use_alpha_versions


@simple_filter
def latest_volto(use_alpha_versions: str) -> str:
    """Return the latest volto version."""
    include_alphas = False if use_alpha_versions.lower() == "no" else True
    url: str = "https://registry.npmjs.org/@plone/volto"
    resp = requests.get(url, headers={"Accept": "application/vnd.npm.install-v1+json"})
    data = resp.json()
    versions = [version for version in data["dist-tags"].values()]
    return latest_version(versions, VOLTO_MIN_VERSION, include_alphas=include_alphas)


@simple_filter
def latest_volto_generator(volto_version) -> str:
    """Return the latest volto generator version."""
    url: str = "https://registry.npmjs.org/@plone/generator-volto"
    resp = requests.get(url, headers={"Accept": "application/vnd.npm.install-v1+json"})
    data = resp.json()
    versions = [version for version in data["dist-tags"].values()]
    return latest_version(
        versions, VOLTO_GENERATOR_MIN_VERSION, include_alphas="-" in volto_version
    )


@simple_filter
def latest_plone(v) -> str:
    """Return the latest plone version."""
    url: str = "https://dist.plone.org/release/6.0-latest/constraints.txt"
    resp = requests.get(url)
    data = resp.content.decode("utf-8")
    return re.search("\nPlone==(.*)\n", data).groups()[0]


@simple_filter
def node_version(volto_version: str) -> int:
    """Return the Node Version to be used."""
    major = int(volto_version.split(".")[0])
    return VOLTO_NODE.get(major, DEFAULT_NODE)


@simple_filter
def gs_language_code(code: str) -> str:
    """Return the language code as expected by Generic Setup."""
    gs_code = code.lower()
    if "-" in code:
        base_language, country = code.split("-")
        gs_code = f"{base_language}-{country.lower()}"
    return gs_code


@simple_filter
def locales_language_code(code: str) -> str:
    """Return the language code as expected by gettext."""
    gs_code = code.lower()
    if "-" in code:
        base_language, country = code.split("-")
        gs_code = f"{base_language}_{country.upper()}"
    return gs_code


@simple_filter
def docker_image_prefix(registry: str) -> str:
    """Return the a prefix to be used with all Docker images."""
    return REGISTRIES.get(registry, "")


@simple_filter
def pascal_case(package_name: str) -> str:
    """Return the package name as a string in the PascalCase format ."""
    parts = [name.title() for name in package_name.split("_")]
    return "".join(parts)


@simple_filter
def extract_host(hostname: str) -> str:
    """Get the host part of a hostname."""
    parts = hostname.split(".")
    return parts[0]
