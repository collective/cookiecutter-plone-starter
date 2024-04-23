"""Post generation hook."""

import json
import os
import subprocess
import sys
from pathlib import Path
from textwrap import dedent

from cookiecutter.utils import rmtree

TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m"
INFO = "\x1b[1;34m"
HINT = "\x1b[3;35m"
SUCCESS = "\x1b[1;32m"
ERROR = "\x1b[1;31m"
MSG_DELIMITER = "=" * 80
MSG_DELIMITER_2 = "-" * 80


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
const applyConfig = (config) => {
  config.settings = {
    ...config.settings,
    isMultilingual: false,
    supportedLanguages: ['{{ cookiecutter.language_code }}'],
    defaultLanguage: '{{ cookiecutter.language_code }}',
  };
  return config;
};

export default applyConfig;
"""


VOLTO_ADDONS = [
    "@eeacms/volto-accordion-block",
    "@kitconcept/volto-slider-block",
    "@eeacms/volto-matomo",
]


def run_cmd(command: str, shell: bool, cwd: str) -> bool:
    proc = subprocess.run(command, shell=shell, cwd=cwd, capture_output=True)
    if proc.returncode:
        # Write errors to the main process stderr
        print(_error(f"\nError while running {command}:"), file=sys.stderr)
        sys.stderr.buffer.write(proc.stderr)
        print("\n", file=sys.stderr)
    return False if proc.returncode else True


DEVOPS_TO_REMOVE = {
    "ansible": [
        "devops/.env_dist",
        "devops/.gitignore",
        "devops/ansible.cfg",
        "devops/etc",
        "devops/inventory",
        "devops/Makefile",
        "devops/playbooks",
        "devops/requirements",
        "devops/tasks",
        "devops/README.md",
    ],
    "gha": [
        ".github/workflows/manual_deploy.yml",
        "devops/.env_gha",
        "devops/README-GHA.md",
    ],
    "cache": [
        ".github/workflows/varnish.yml",
        "backend/src/{{ cookiecutter.python_package_name }}/src/{{ cookiecutter.python_package_name }}/profiles/default/registry/plone.cachepurging.interfaces.ICachePurgingSettings.xml",
        "backend/src/{{ cookiecutter.python_package_name }}/src/{{ cookiecutter.python_package_name }}/profiles/default/registry/plone.caching.interfaces.ICacheSettings.xml",
        "devops/varnish",
    ],
}


def prepare_devops():
    """Clean up devops."""
    keep_ansible = int("{{ cookiecutter.devops_ansible }}")
    keep_gha_manual_deploy = int("{{ cookiecutter.devops_gha_deploy }}")
    keep_cache = int("{{ cookiecutter.devops_cache }}")
    to_remove = []
    if not keep_ansible:
        to_remove.extend(DEVOPS_TO_REMOVE["ansible"])
    if not keep_gha_manual_deploy:
        to_remove.extend(DEVOPS_TO_REMOVE["gha"])
    if not keep_cache:
        to_remove.extend(DEVOPS_TO_REMOVE["cache"])
    for filepath in to_remove:
        path = Path(filepath)
        exists = path.exists()
        if exists and path.is_dir():
            rmtree(path)
        elif exists and path.is_file():
            path.unlink()


def get_npm_global_packages() -> dict:
    """List all globally installed NPM packages."""
    cwd = Path()
    command = "npm ls --json -g"
    proc = subprocess.run(command, shell=True, cwd=cwd, capture_output=True)
    if proc.returncode:
        return {}

    try:
        response = json.loads(proc.stdout)
    except json.JSONDecodeError:
        response = {}
    return response.get("dependencies", {})


def npm_packages_to_install(volto_generator_version: str) -> list:
    """Return a list of packages to be installed globally."""
    to_install = []
    installed = get_npm_global_packages()
    to_check = [("yo", "*"), ("@plone/generator-volto", volto_generator_version)]
    for package_name, version in to_check:
        version = None if version == "*" else version
        package_identifier = f"{package_name}@{version}" if version else package_name

        # Check if the package is already installed or with a distinct version
        installed_version = installed.get(package_name, {}).get("version", None)
        if not installed_version or (version and version != installed_version):
            to_install.append(package_identifier)
    return to_install


def prepare_frontend(
    volto_version: str,
    volto_generator_version: str,
    description: str,
    volto_addon_name: str,
):
    """Run volto generator."""
    print("Frontend codebase:")
    canary = (
        " --canary"
        if [x for x in ("alpha", "beta", "rc") if x in volto_version]
        else ""
    )
    generator_steps = {
        "v7": [
            [
                f"Generate frontend application with @plone/volto {_info(volto_version)}",
                f"yo @plone/volto frontend --description '{description}' "
                f"--skip-install --no-interactive --volto={volto_version}{canary}",
                True,
                "frontend",
            ],
            [
                f"Generate addon {volto_addon_name}",
                f"yo @plone/volto:addon {volto_addon_name} --interactive false --skip-install",
                True,
                "frontend",
            ],
        ],
        "v8": [
            [
                f"Generate frontend application with @plone/volto {_info(volto_version)}",
                f"yo @plone/volto frontend --description '{description}' "
                f"--skip-install --no-interactive --volto={volto_version}{canary} "
                f"--defaultAddonName {volto_addon_name}",
                True,
                "frontend",
            ],
        ],
    }
    _generator_family = (
        "v8" if int(volto_generator_version.split(".")[0]) >= 8 else "v7"
    )
    steps = generator_steps.get(_generator_family)
    to_install = npm_packages_to_install(volto_generator_version)
    if to_install:
        cmd = [
            "npm",
            "install",
            "--no-audit",
            "--no-fund",
            "-g",
        ]
        cmd.extend(to_install)
        steps.insert(
            0,
            [
                f"Installing required npm packages",
                cmd,
                sys.platform.startswith("win"),
                "frontend",
            ],
        )

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
    # Include addons on the volto-addon we created
    addon_path = (Path("frontend") / "src" / "addons" / volto_addon_name).resolve()
    addon_package_json = addon_path / "package.json"
    package_data = json.loads(addon_package_json.read_text())
    _addons = package_data.get("addons", [])
    _deps = package_data.get("dependencies", {})
    for addon in VOLTO_ADDONS:
        _addons.append(addon)
        _deps[addon] = "*"
    package_data["addons"] = _addons
    package_data["dependencies"] = _deps
    addon_package_json.write_text(json.dumps(package_data, indent=2))
    # And add language code settings
    cfg = addon_path / "src" / "index.js"
    cfg.write_text(VOLTO_CONFIG)


PYTHON_TEST_PATHS_TO_REMOVE = {
    "pytest": [
        "src/{{ cookiecutter.python_package_name }}/src/{{ cookiecutter.python_package_name }}/tests"
    ],
    "unittest": ["src/{{ cookiecutter.python_package_name }}/tests"],
}


def clean_up_backend_tests():
    folders = PYTHON_TEST_PATHS_TO_REMOVE["{{ cookiecutter.python_test_framework }}"]
    for folder in folders:
        msg = f"Remove folder {folder} not used by {{ cookiecutter.python_test_framework }}"
        command = ["rm", "-Rf", folder]
        shell = False
        cwd = "backend"
        print(f" - {msg}")
        result = run_cmd(command, shell=shell, cwd=cwd)
        if not result:
            sys.exit(1)


def prepare_backend():
    """Apply black and isort to the generated codebase."""
    print("Backend codebase")
    # Clean up unused test folders
    clean_up_backend_tests()
    steps = [
        ["Format generated code in the backend", ["make", "format"], False, "backend"]
    ]
    for step in steps:
        msg, command, shell, cwd = step
        print(f" - {msg}")
        run_cmd(command, shell=shell, cwd=cwd)
        # Note: we intentionally don't exit if formatting fails.


volto_version = "{{ cookiecutter.volto_version }}"
volto_generator_version = "{{ cookiecutter.volto_generator_version }}"
volto_addon_name = "{{ cookiecutter.volto_addon_name }}"
description = "{{ cookiecutter.description }}"


def main():
    """Final fixes."""
    # Setup Devops
    prepare_devops()
    # Setup frontend
    prepare_frontend(
        volto_version=volto_version,
        volto_generator_version=volto_generator_version,
        description=description,
        volto_addon_name=volto_addon_name,
    )
    print("")
    # Setup backend
    prepare_backend()
    print("")
    print(f"{MSG_DELIMITER}")
    msg = dedent(
        f"""
        {_success('Project "{{ cookiecutter.project_title }}" was generated')}
        {MSG_DELIMITER_2}
        Now, code it, create a git repository, push to your organization.

        Sorry for the convenience,
        The Plone Community.
    """
    )
    print(msg)
    print(f"{MSG_DELIMITER}")


if __name__ == "__main__":
    main()
