"""Test cookiecutter generation."""
import pytest

from hooks import pre_gen_project


@pytest.mark.parametrize(
    "value,expected",
    (
        ("   ", "should be provided"),
        (" ", "should be provided"),
        ("", "should be provided"),
        ("\t", "should be provided"),
        ("bar", ""),
        ("foo", ""),
    ),
)
def test_validate_not_empty(value: str, expected: str):
    """Test validate_not_empty function."""
    result = pre_gen_project.validate_not_empty(value)
    assert result == expected


@pytest.mark.parametrize(
    "value,expected",
    (
        (" ", "' ' is not a valid language code."),
        ("", "'' is not a valid language code."),
        ("en", ""),
        ("en-us", ""),
        ("pt-br", ""),
        ("en-", "'en-' is not a valid language code."),
        ("EN-", "'EN-' is not a valid language code."),
        ("EN-99", "'EN-99' is not a valid language code."),
    ),
)
def test_validate_language_code(value: str, expected: str):
    """Test validate_language_code function."""
    result = pre_gen_project.validate_language_code(value)
    assert result == expected


@pytest.mark.parametrize(
    "value,expected",
    (
        (" ", "' ' is not a valid Plone version."),
        ("-", "'-' is not a valid Plone version."),
        ("", "'' is not a valid Plone version."),
        ("5.2.8", "'5.2.8' is not a valid Plone version."),
        ("6.0.0", ""),
        ("6.0.0a4", ""),
        ("6.0.0b1", ""),
        ("6.0.0rc1", ""),
        ("6.0.1", ""),
        ("6.1.0", ""),
        ("6.1.10", ""),
        ("6.10.1", ""),
        ("6.10.10", ""),
    ),
)
def test_validate_plone_version(value: str, expected: str):
    """Test validate_plone_version function."""
    result = pre_gen_project.validate_plone_version(value)
    assert result == expected


@pytest.mark.parametrize(
    "value,expected",
    (
        (" ", "' ' is not a valid Volto version."),
        ("-", "'-' is not a valid Volto version."),
        ("", "'' is not a valid Volto version."),
        ("14.10.0", "'14.10.0' is not a valid Volto version."),
        ("15.0.0", ""),
        ("15.0.10", ""),
        ("15.10.1", ""),
        ("16.0.0-alpha.12", ""),
        ("16.0.0-alpha.4", ""),
        ("16.0.0-beta.1", ""),
        ("16.0.1-beta.1", ""),
    ),
)
def test_validate_volto_version(value: str, expected: str):
    """Test validate_volto_version function."""
    result = pre_gen_project.validate_volto_version(value)
    assert result == expected


@pytest.mark.parametrize(
    "value,expected",
    (
        (" ", "' ' is not a valid Python identifier."),
        ("", "'' is not a valid Python identifier."),
        ("project title", "'project title' is not a valid Python identifier."),
        ("project_title", ""),
        ("project-title", "'project-title' is not a valid Python identifier."),
        ("projecttitle", ""),
        ("projectTitle", ""),
    ),
)
def test_validate_python_package_name(value: str, expected: str):
    """Test validate_python_package_name function."""
    result = pre_gen_project.validate_python_package_name(value)
    assert result == expected


def test_validate_python_package_name(bad_context: dict):
    """Test check_errors function."""
    errors = pre_gen_project.check_errors(bad_context)
    assert errors
    assert len(errors) == 4


@pytest.mark.parametrize(
    "value,expected",
    (
        ("v16.13.1", "16"),
        ("v14.0.0", "14"),
    ),
)
def test_node_major_version(value, expected):
    """Test node_major_version."""
    func = pre_gen_project.node_major_version
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
    func = pre_gen_project.docker_version
    assert func(value) == expected
