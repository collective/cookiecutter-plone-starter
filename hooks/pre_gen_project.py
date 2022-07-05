"""Pre generation hook."""
import re
import subprocess
import sys
from os import stat
from pathlib import Path
from textwrap import dedent
from typing import List

TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m"
INFO = "\x1b[1;34m"
HINT = "\x1b[3;35m"
SUCCESS = "\x1b[1;32m"
ERROR = "\x1b[1;31m"
MSG_DELIMITER = "=" * 80
SEMVER_PATTERN = r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"  # noQA
PEP404_PATTERN = r"^(\d+!)?(\d+)(\.\d+)+([\.\-\_])?((a(lpha)?|b(eta)?|c|r(c|ev)?|pre(view)?)\d*)?(\.?(post|dev)\d*)?$"  # noQA


def _error(msg: str) -> str:
    """Format error message."""
    return f"{ERROR}{msg}{TERMINATOR}"


def _success(msg: str) -> str:
    """Format success message."""
    return f"{SUCCESS}{msg}{TERMINATOR}"


def _warning(msg: str) -> str:
    """Format warning message."""
    return f"{WARNING}{msg}{TERMINATOR}"


def _info(msg: str) -> str:
    """Format info message."""
    return f"{INFO}{msg}{TERMINATOR}"


SUPPORTED_PYTHON_VERSIONS = [
    "3.7",
    "3.8",
    "3.9",
    "3.10",
]


SUPPORTED_NODE_VERSION = [
    "16",
]

output_path = Path().resolve()

context = {
    "project_title": "{{ cookiecutter.project_title }}",
    "project_slug": "{{ cookiecutter.project_slug }}",
    "description": "{{ cookiecutter.description }}",
    "author": "{{ cookiecutter.author }}",
    "email": "{{ cookiecutter.email }}",
    "python_package_name": "{{ cookiecutter.python_package_name }}",
    "plone_version": "{{ cookiecutter.plone_version }}",
    "volto_version": "{{ cookiecutter.volto_version }}",
    "language_code": "{{ cookiecutter.language_code }}",
    "github_organization": "{{ cookiecutter.github_organization }}",
    "container_registry": "{{ cookiecutter.container_registry }}",
}


def validate_not_empty(value: str) -> str:
    """Value should not be empty."""
    return "" if value.strip() else "should be provided"


def validate_plone_version(value: str) -> str:
    """Plone version should be superior to 6."""
    match = re.match(PEP404_PATTERN, value)
    valid = match and value.startswith("6.")
    return "" if valid else f"'{value}' is not a valid Plone version."


def validate_volto_version(value: str) -> str:
    """Volto version should be superior to 15."""
    match = re.match(SEMVER_PATTERN, value)
    valid = match and int(value.split(".")[0]) >= 15
    return "" if valid else f"'{value}' is not a valid Volto version."


def validate_language_code(value: str) -> str:
    """Language code should be valid."""
    pattern = r"^([a-z]{2}|[a-z]{2}-[a-z]{2})$"
    return (
        "" if re.match(pattern, value) else f"'{value}' is not a valid language code."
    )


def validate_python_package_name(value: str) -> str:
    """Validate python_package_name is an identifier."""
    return (
        "" if value.isidentifier() else f"'{value}' is not a valid Python identifier."
    )


VALIDATORS = {
    name: func for name, func in locals().items() if name.startswith("validate_")
}


def node_major_version(value: str) -> str:
    """Parse value and return the major version."""
    value = value.strip()
    match = re.match(r"v(\d{1,3})\.\d{1,3}.\d{1,3}", value)
    return match.groups()[0] if match else ""


def check_python_version() -> str:
    """Check if Python version is supported."""
    version = f"{sys.version_info.major}.{sys.version_info.minor}"
    return (
        ""
        if version in SUPPORTED_PYTHON_VERSIONS
        else f"Python version is not supported: Got {sys.version}"
    )


def check_node_version() -> str:
    """Check if node version is supported."""
    try:
        raw_version = subprocess.run(
            ["node", "--version"], capture_output=True
        ).stdout.decode()
    except FileNotFoundError:
        return "NodeJS not found."
    else:
        version = node_major_version(raw_version)
        return (
            ""
            if version in SUPPORTED_NODE_VERSION
            else f"Node version is not supported: Got {raw_version}"
        )


def sanity_check() -> bool:
    """Run sanity checks on the system."""
    checks = {
        "Python": {"func": check_python_version, "level": "error"},
        "Node": {"func": check_node_version, "level": "error"},
    }
    has_error = False
    print("Running sanity checks")
    for title, check_info in checks.items():
        func = check_info["func"]
        status = func()
        level = check_info["level"]
        if status:
            has_error = has_error and (level == "error")
            msg = f"{_error(status)}"
        else:
            msg = f"{_success('✓')}"
        print(f"  - {title}: {msg}")
    return not (has_error)


def check_errors(data: dict) -> List[str]:
    """Check for errors in the provided data."""
    errors = []
    for key, value in data.items():
        func = VALIDATORS.get(f"validate_{key}", validate_not_empty)
        error = func(value)
        if error:
            errors.append(f"  - {key}: {_error(error)}")
    return errors


def main():
    """Validate context."""
    success = True
    value_errors = check_errors(context)
    print(f"{MSG_DELIMITER}")
    print(f"{ _info('{{ cookiecutter.project_title }} generation')}")
    print(f"{MSG_DELIMITER}")
    if not sanity_check():
        success = False
    elif value_errors:
        print("Value errors prevent running cookiecutter")
        for error in value_errors:
            print(error)
        success = False
    else:
        msg = dedent(
            f"""
            Summary:
              - Plone version: {_info('{{ cookiecutter.plone_version }}')}
              - Volto version: {_info('{{ cookiecutter.volto_version }}')}
              - Output folder: {_info(output_path)}
        """
        )

        print(msg)
    if not success:
        print(f"{MSG_DELIMITER}")
        sys.exit(1)


if __name__ == "__main__":
    main()
