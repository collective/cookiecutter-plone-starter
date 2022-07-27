"""Post generation hook."""
import os
import re
import subprocess
import sys
from pathlib import Path
from textwrap import dedent

TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m"
INFO = "\x1b[1;34m"
HINT = "\x1b[3;35m"
SUCCESS = "\x1b[1;32m"
ERROR = "\x1b[1;31m"
MSG_DELIMITER = "=" * 80


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


VOLTO_CONFIG = """
  config.settings = {
    ...config.settings,
    isMultilingual: false,
    supportedLanguages: ['{{ cookiecutter.language_code }}'],
    defaultLanguage: '{{ cookiecutter.language_code }}',
  };
"""


VOLTO_ADDONS = [
    "volto-slate:minimalDefault,simpleLink",
    "@eeacms/volto-accordion-block",
    "@kitconcept/volto-blocks-grid",
    "@kitconcept/volto-slider-block",
    "@eeacms/volto-matomo",
]


def prepare_frontend(volto_version: str, description: str):
    """Run volto generator."""
    print("Frontend codebase:")
    addons = " ".join([f"--addon {item}" for item in VOLTO_ADDONS])
    steps = [
        [
            f"Install latest {_info('@plone/generator-volto')}",
            [
                "npm",
                "install",
                "--no-audit",
                "--no-fund",
                "-g",
                "yo",
                "@plone/generator-volto",
            ],
            sys.platform.startswith("win"),
            "frontend",
        ],
        [
            f"Generate frontend application with @plone/volto {_info(volto_version)}",
            f"yo @plone/volto frontend --description '{description}' {addons} "
            f"--skip-install --no-interactive --volto={volto_version}",
            True,
            "frontend",
        ],
    ]
    for step in steps:
        msg, command, shell, cwd = step
        print(f" - {msg}")
        proc = subprocess.run(command, shell=shell, cwd=cwd, capture_output=True)
    # Rename template files
    frontend_path = Path("frontend").resolve()
    for src in frontend_path.glob("*.default"):
        dst_filename = src.name.replace(".default", "")
        dst = (frontend_path / dst_filename).resolve()
        os.rename(src, dst)
    # Add language code setting
    cfg = (Path("frontend") / "src" / "config.js").resolve()
    with open(cfg, "r") as fh:
        data = fh.read()
    with open(cfg, "w") as fh:
        new_data = re.sub("\n  \/\/ Add here your project.*\n", VOLTO_CONFIG, data)
        fh.write(new_data)


def prepare_backend():
    """Apply black and isort to the generated codebase."""
    print("Backend codebase")
    steps = [
        ["Format generated code in the backend", ["make", "format"], False, "backend"]
    ]
    for step in steps:
        msg, command, shell, cwd = step
        print(f" - {msg}")
        proc = subprocess.run(command, shell=shell, cwd=cwd, capture_output=True)


volto_version = "{{ cookiecutter.volto_version }}"
description = "{{ cookiecutter.description }}"


def main():
    """Final fixes."""
    prepare_frontend(volto_version=volto_version, description=description)
    print("")
    prepare_backend()
    print(f"{MSG_DELIMITER}")
    msg = dedent(
        f"""
        {_success('Project "{{ cookiecutter.project_title }}" was generated')}

        Now, code it, create a git repository, push to your organization.

        Sorry for the convenience,
        The Plone Community.
    """
    )
    print(msg)
    print(f"{MSG_DELIMITER}")


if __name__ == "__main__":
    main()
