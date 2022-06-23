"""Pre generation hook."""
import re
import sys
from pathlib import Path
from textwrap import dedent
from typing import List

TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "
MSG_DELIMITER = "=" * 50
SEMVER_PATTERN = r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"  # noQA
PEP404_PATTERN = r"^(\d+!)?(\d+)(\.\d+)+([\.\-\_])?((a(lpha)?|b(eta)?|c|r(c|ev)?|pre(view)?)\d*)?(\.?(post|dev)\d*)?$"  # noQA

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


def check_errors(data: dict) -> List[str]:
    """Check for errors in the provided data."""
    errors = []
    for key, value in data.items():
        func = VALIDATORS.get(f"validate_{key}", validate_not_empty)
        error = func(value)
        if error:
            errors.append(f"{key}: {error}")
    return errors


def main():
    """Validate context."""
    errors = check_errors(context)
    if errors:
        print(f"{MSG_DELIMITER}")
        print("Value errors prevent running cookiecutter")
        for error in errors:
            print(f"  - {error}")
        print(f"{MSG_DELIMITER}")
        sys.exit(1)

    msg = dedent(
        f"""
        {MSG_DELIMITER}
        Starting "{{ cookiecutter.project_title }}" generation
        Plone version: {{ cookiecutter.plone_version }}
        Volto version: {{ cookiecutter.volto_version }}
        Output folder: {output_path}
        {MSG_DELIMITER}
    """
    )

    print(msg)


if __name__ == "__main__":
    main()
