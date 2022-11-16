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
    "@eeacms/volto-accordion-block",
    "@kitconcept/volto-blocks-grid",
    "@kitconcept/volto-slider-block",
    "@eeacms/volto-matomo",
]


def run_cmd(command: str, shell: bool, cwd: str) -> bool:
    proc = subprocess.run(command, shell=shell, cwd=cwd, capture_output=True)
    if proc.returncode:
        # Create log on the folder containing the project
        log_file = Path("../plone_starter_error.log").resolve()
        log_file.write_bytes(proc.stderr)
        print(_error(f"There was an error, see {log_file} for details"))
    return False if proc.returncode else True


def prepare_frontend(
    volto_version: str, volto_generator_version: str, description: str
):
    """Run volto generator."""
    print("Frontend codebase:")
    addons = " ".join([f"--addon {item}" for item in VOLTO_ADDONS])
    canary = (
        " --canary"
        if [x for x in ("alpha", "beta", "rc") if x in volto_version]
        else ""
    )
    generator_version_literal = f"@plone/generator-volto@{volto_generator_version}"
    steps = [
        [
            f"Installing {_info(generator_version_literal)}",
            [
                "npm",
                "install",
                "--no-audit",
                "--no-fund",
                "-g",
                "yo",
                f"@plone/generator-volto@{volto_generator_version}",
            ],
            sys.platform.startswith("win"),
            "frontend",
        ],
        [
            f"Generate frontend application with @plone/volto {_info(volto_version)}",
            f"yo @plone/volto frontend --description '{description}' {addons} "
            f"--skip-install --no-interactive --volto={volto_version}{canary}",
            True,
            "frontend",
        ],
    ]
    for step in steps:
        msg, command, shell, cwd = step
        print(f" - {msg}")
        result = run_cmd(command, shell=shell, cwd=cwd)
        if not result:
            sys.exit(1)

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
        result = run_cmd(command, shell=shell, cwd=cwd)
        if not result:
            sys.exit(1)


volto_version = "{{ cookiecutter.volto_version }}"
volto_generator_version = "{{ cookiecutter.volto_generator_version }}"
description = "{{ cookiecutter.description }}"


def main():
    """Final fixes."""
    prepare_frontend(
        volto_version=volto_version,
        volto_generator_version=volto_generator_version,
        description=description,
    )
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
