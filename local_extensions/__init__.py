import os
import re
from typing import List, Optional

import requests
from cookiecutter.utils import simple_filter

from .semver import VersionInfo

REGISTRIES = {
    "Docker Hub": "",
    "GitHub": "ghcr.io/",
}


VOLTO_MIN_VERSION = 16


VOLTO_GENERATOR_VERSIONS = {
    16: (6, 7),
    17: (7, 9),
    18: (9, None),
}


DEFAULT_NODE = 18

VOLTO_NODE = {
    16: 16,
    17: DEFAULT_NODE,
    18: 20,
}


def _major_version(version: str) -> int:
    version = version[1:] if version.startswith("v") else version
    return int(version.split(".")[0])


def _check_version(
    version: str, min_version: Optional[int] = None, max_version: Optional[int] = None
) -> bool:
    """Check if a version is supported."""
    is_valid = True
    major = _major_version(version)
    if min_version:
        is_valid = is_valid and (major >= min_version)
    if max_version:
        is_valid = is_valid and (major < max_version)
    return is_valid


def latest_version(
    versions: List[str],
    min_version: Optional[int] = None,
    max_version: Optional[int] = None,
    include_alphas: bool = False,
):
    valid = sorted(
        [
            v
            for v in versions
            if _check_version(
                version=v, min_version=min_version, max_version=max_version
            )
        ],
        key=lambda v: VersionInfo.parse(v.replace("v", "")),
        reverse=True,
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
    return latest_version(
        versions, min_version=VOLTO_MIN_VERSION, include_alphas=include_alphas
    )


@simple_filter
def latest_volto_generator(raw_volto_version: str) -> str:
    """Return the latest volto generator version."""
    url: str = "https://registry.npmjs.org/@plone/generator-volto"
    resp = requests.get(url, headers={"Accept": "application/vnd.npm.install-v1+json"})
    data = resp.json()
    # Reverse list to get latest versions first
    versions = [version for version in data["versions"].keys()][::-1]
    # Get min and max versions for a given volto version
    major = _major_version(raw_volto_version)
    min_version, max_version = VOLTO_GENERATOR_VERSIONS.get(major)
    include_alphas = "-" in raw_volto_version
    return latest_version(
        versions,
        min_version=min_version,
        max_version=max_version,
        include_alphas=include_alphas,
    )


@simple_filter
def latest_plone(v: str) -> str:
    """Return the latest plone version."""
    url: str = "https://dist.plone.org/release/6.0-latest/constraints.txt"
    resp = requests.get(url)
    data = resp.content.decode("utf-8")
    return re.search("\nPlone==(.*)\n", data).groups()[0]


@simple_filter
def node_version(volto_version: str) -> int:
    """Return the Node Version to be used."""
    major = _major_version(volto_version)
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
