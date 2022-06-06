"""Post generation hook."""
import os
import subprocess
import sys
from pathlib import Path
from textwrap import dedent

TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m"
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "


VOLTO_ADDONS = [
    "volto-slate:minimalDefault,simpleLink",
    "@eeacms/volto-accordion-block",
    "@kitconcept/volto-blocks-grid",
    "@kitconcept/volto-slider-block",
    "@eeacms/volto-matomo",
]


def print_info(msg: str, prefix: str = "[INFO]: "):
    """Print a INFO message."""
    print(f"{prefix}{msg}{TERMINATOR}")


def prepare_frontend(volto_version: str, description: str):
    """Run volto generator."""
    print_info("Prepare frontend codebase")
    addons = " ".join([f"--addon {item}" for item in VOLTO_ADDONS])
    steps = [
        [
            "Install latest @plone/generator-volto",
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
            f"Generate frontend application with @plone/volto {volto_version}",
            f"yo @plone/volto frontend --description '{description}' {addons} "
            f"--skip-install --no-interactive --volto={volto_version}",
            True,
            "frontend",
        ],
    ]
    for step in steps:
        msg, command, shell, cwd = step
        print_info(f"{msg}", "  -- ")
        proc = subprocess.run(command, shell=shell, cwd=cwd, capture_output=True)
    # Rename Makefile.default to Makefile
    src = (Path("frontend") / "Makefile.default").resolve()
    dst = (Path("frontend") / "Makefile").resolve()
    os.rename(src, dst)


def prepare_backend():
    """Apply black and isort to the generated codebase."""
    print_info("Prepare backend codebase")
    steps = [
        ["Format generated code in the backend", ["make", "format"], False, "backend"]
    ]
    for step in steps:
        msg, command, shell, cwd = step
        print_info(f"{msg}", "  -- ")
        proc = subprocess.run(command, shell=shell, cwd=cwd, capture_output=True)


volto_version = "{{ cookiecutter.volto_version }}"
description = "{{ cookiecutter.description }}"
prepare_frontend(volto_version=volto_version, description=description)
prepare_backend()


msg = dedent(
    """
    ===============================================================================
    Project "{{ cookiecutter.project_title }}" was generated.
    Now, code it, create a git repository, push to your organization.
    Sorry for the convenience.
    ===============================================================================
"""
)

print(msg)
