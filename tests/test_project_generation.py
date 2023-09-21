"""Test Generator: / and /devops."""
import json

import pytest
import yaml


@pytest.mark.parametrize(
    "filepath",
    [
        ".editorconfig",
        ".github/workflows/backend.yml",
        ".github/workflows/frontend.yml",
        ".gitignore",
        ".vscode/settings.json",
        "CHANGELOG.md",
        "devops/.env_dev",
        "devops/.gitignore",
        "devops/ansible.cfg",
        "devops/group_vars/all/groups.yml",
        "devops/group_vars/all/host.yml",
        "devops/group_vars/all/swap.yml",
        "devops/group_vars/all/ufw.yml",
        "devops/group_vars/all/users.yml",
        "devops/host_vars/plone.org.br-local.yml",
        "devops/Makefile",
        "devops/playbook-setup.yml",
        "devops/README.md",
        "devops/stacks/plone.yml",
        "devops/Vagrantfile",
        "docker-compose.yml",
        "Makefile",
        "README.md",
        "version.txt",
    ],
)
def test_project_files(cutter_result, filepath: str):
    """Test created files."""
    folder = cutter_result.project_path
    path = folder / filepath
    assert path.is_file()


@pytest.mark.parametrize(
    "filepath",
    [
        ".github/workflows/backend.yml",
        ".github/workflows/frontend.yml",
        "devops/group_vars/all/groups.yml",
        "devops/group_vars/all/host.yml",
        "devops/group_vars/all/swap.yml",
        "devops/group_vars/all/ufw.yml",
        "devops/group_vars/all/users.yml",
        "devops/host_vars/plone.org.br-local.yml",
        "devops/playbook-setup.yml",
        "devops/stacks/plone.yml",
        "docker-compose.yml",
    ],
)
def test_valid_yaml_files(cutter_result, filepath: str):
    """Test generated yaml files are valid."""
    folder = cutter_result.project_path
    path = folder / filepath
    with open(path, "r") as fh:
        content = yaml.full_load(fh)
    assert content


@pytest.mark.parametrize(
    "filepath",
    [
        "frontend/mrs.developer.json",
        "frontend/package.json",
        "frontend/tsconfig.json",
        "frontend/cypress/fixtures/example.json",
        "frontend/src/addons/volto-ploneorgbr/.release-it.json",
        "frontend/src/addons/volto-ploneorgbr/package.json",
        "frontend/src/addons/volto-ploneorgbr/acceptance/package.json",
        "frontend/src/addons/volto-ploneorgbr/acceptance/cypress/fixtures/example.json",
        ".vscode/settings.json",
    ],
)
def test_valid_json_files(cutter_result, filepath: str):
    """Test generated json files are valid."""
    folder = cutter_result.project_path
    path = folder / filepath
    with open(path, "r") as fh:
        content = json.load(fh)
    assert content
