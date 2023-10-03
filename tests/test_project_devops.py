"""Test Generator: /devops."""
import pytest
import yaml

ANSIBLE_FILES = [
    "devops/.env_dist",
    "devops/.gitignore",
    "devops/ansible.cfg",
    "devops/etc/docker/daemon/daemon.json.j2",
    "devops/etc/docker/systemd/http-proxy.conf.j2",
    "devops/etc/keys/.gitkeep",
    "devops/inventory/group_vars/all/base.yml",
    "devops/inventory/group_vars/all/docker.yml",
    "devops/inventory/group_vars/all/packages.yml",
    "devops/inventory/group_vars/all/projects.yml",
    "devops/inventory/group_vars/all/sshd.yml",
    "devops/inventory/group_vars/all/swap.yml",
    "devops/inventory/group_vars/all/ufw.yml",
    "devops/inventory/group_vars/all/users.yml",
    "devops/inventory/hosts.yml",
    "devops/Makefile",
    "devops/playbooks/setup.yml",
    "devops/README.md",
    "devops/requirements/collections.yml",
    "devops/requirements/requirements.txt",
    "devops/requirements/roles.yml",
    "devops/tasks/base/task_base_packages.yml",
    "devops/tasks/base/task_base_python.yml",
    "devops/tasks/base/task_docker.yml",
    "devops/tasks/base/task_hostname.yml",
    "devops/tasks/base/task_ufw.yml",
    "devops/tasks/handlers/common.yml",
    "devops/tasks/swarm/task_swarm.yml",
]

GHA_ACTIONS_CI = [
    ".github/workflows/backend.yml",
    ".github/workflows/frontend.yml",
]

GHA_ACTIONS_DEPLOY = [
    ".github/workflows/manual_deploy.yml",
    "devops/.env_gha",
    "devops/README-GHA.md",
]

STACKS = [
    "devops/stacks/plone.org.br.yml",
    "docker-compose.yml",
]

DEVOPS_FILES = ANSIBLE_FILES + GHA_ACTIONS_CI + GHA_ACTIONS_DEPLOY + STACKS


@pytest.mark.parametrize("filepath", DEVOPS_FILES)
def test_project_devops_files(cutter_result, filepath: str):
    """Test created files."""
    folder = cutter_result.project_path
    path = folder / filepath
    assert path.is_file()


@pytest.mark.parametrize(
    "filepath",
    [filepath for filepath in DEVOPS_FILES if filepath.endswith(".yml")],
)
def test_valid_yaml_files(cutter_result, filepath: str):
    """Test generated yaml files are valid."""
    folder = cutter_result.project_path
    path = folder / filepath
    with open(path, "r") as fh:
        content = yaml.full_load(fh)
    assert content


@pytest.mark.parametrize("filepath", ANSIBLE_FILES)
def test_project_devops_no_ansible(cutter_result_devops_no_ansible, filepath: str):
    """Test Ansible files are not present."""
    folder = cutter_result_devops_no_ansible.project_path
    path = folder / filepath
    assert path.exists() is False


@pytest.mark.parametrize("filepath", GHA_ACTIONS_DEPLOY)
def test_project_devops_no_gha_deploy(
    cutter_result_devops_no_gha_deploy, filepath: str
):
    """Test GHA deploy files are not present."""
    folder = cutter_result_devops_no_gha_deploy.project_path
    path = folder / filepath
    assert path.exists() is False
