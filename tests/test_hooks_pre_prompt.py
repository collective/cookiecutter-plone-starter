"""Test cookiecutter generation."""

import pytest

from hooks import pre_prompt


@pytest.mark.parametrize(
    "value,expected",
    (
        ("v16.13.1", "16"),
        ("v14.0.0", "14"),
    ),
)
def test_node_major_version(value, expected):
    """Test node_major_version."""
    func = pre_prompt.node_major_version
    assert func(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    (
        ("Docker version 20.10.17, build 100c701", "20.10"),
        ("Docker version 20.10.15", "20.10"),
    ),
)
def test_docker_version(value, expected):
    """Test docker_version."""
    func = pre_prompt.docker_version
    assert func(value) == expected
