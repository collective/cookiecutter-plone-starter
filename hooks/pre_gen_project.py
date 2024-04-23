"""Pre generation hook."""

import re
import sys
from pathlib import Path
from textwrap import dedent
from typing import List
from urllib.parse import urlparse

TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m"
INFO = "\x1b[1;34m"
HINT = "\x1b[3;35m"
SUCCESS = "\x1b[1;32m"
ERROR = "\x1b[1;31m"
MSG_DELIMITER = "=" * 80
MSG_DELIMITER_2 = "-" * 80
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


output_path = Path().resolve()

context = {
    "project_title": "{{ cookiecutter.project_title }}",
    "project_slug": "{{ cookiecutter.project_slug }}",
    "description": "{{ cookiecutter.description }}",
    "hostname": "{{ cookiecutter.hostname }}",
    "author": "{{ cookiecutter.author }}",
    "email": "{{ cookiecutter.email }}",
    "python_package_name": "{{ cookiecutter.python_package_name }}",
    "volto_addon_name": "{{ cookiecutter.volto_addon_name }}",
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


def validate_hostname(value: str) -> str:
    """Check if hostname is valid."""
    value_with_protocol = f"https://{value}"
    result = urlparse(value_with_protocol)
    valid = str(result.hostname) == value
    return "" if valid else f"'{value}' is not a valid hostname."


VALIDATORS = {
    name: func for name, func in locals().items() if name.startswith("validate_")
}


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
    print("")

    print(f"{ _info('{{ cookiecutter.project_title }} generation')}")
    print(f"{MSG_DELIMITER_2}")
    if value_errors:
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
              - Volto Generator version: {_info('{{ cookiecutter.volto_generator_version }}')}
              - Output folder: {_info(output_path)}
        """
        )

        print(msg)
    if not success:
        print(f"{MSG_DELIMITER}")
        sys.exit(1)


if __name__ == "__main__":
    main()
