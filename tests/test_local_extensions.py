from typing import Any

import pytest
from cookiecutter.environment import StrictEnvironment


@pytest.fixture(scope="session")
def strict_environment():
    """Return an environment with all extensions loaded."""
    context = {
        "cookiecutter": {
            "_extensions": [
                "local_extensions.use_alpha_versions",
                "local_extensions.node_version",
                "local_extensions.extract_host",
                "local_extensions.docker_image_prefix",
                "local_extensions.pascal_case",
                "local_extensions.locales_language_code",
                "local_extensions.gs_language_code",
                "local_extensions.latest_volto",
                "local_extensions.latest_volto_generator",
                "local_extensions.latest_plone",
            ]
        }
    }
    return StrictEnvironment(context=context, keep_trailing_newline=True)


@pytest.fixture()
def filter_test(strict_environment):
    """Test a Jinja2 filter."""

    def func(filter_name: str, value: Any) -> str:
        inner = f" {value} | {filter_name} "
        template = strict_environment.from_string("{{ " + inner + "}}")
        return template.render()

    return func


@pytest.fixture()
def mock_volto_versions_call(requests_mock):
    data = {
        "dist-tags": {"alpha": "18.0.0-alpha.4", "latest": "17.6.1", "lts": "16.28.1"}
    }
    requests_mock.get("https://registry.npmjs.org/@plone/volto", json=data)


@pytest.fixture()
def mock_volto_generator_versions_call(requests_mock):
    data = {
        "versions": {
            "6.4.0": {},
            "7.0.0": {},
            "7.0.1": {},
            "6.4.1": {},
            "8.0.0": {},
            "8.0.3": {},
            "8.1.0": {},
            "9.0.0-alpha.0": {},
            "9.0.0-alpha.1": {},
        }
    }
    requests_mock.get("https://registry.npmjs.org/@plone/generator-volto", json=data)


@pytest.fixture()
def mock_plone_version_call(requests_mock):
    content = b"\nPlone==6.0.8\n"
    requests_mock.get(
        "https://dist.plone.org/release/6.0-latest/constraints.txt", content=content
    )


@pytest.mark.parametrize(
    "version,min_version,max_version,expected",
    (
        ("v16.13.1", 14, None, True),
        ("v16.13.1", 14, 15, False),
        ("16.13.1", 14, 15, False),
        ("16.13.1", None, None, True),
    ),
)
def test_check_version(version: str, min_version, max_version, expected):
    """Test local_extensions._check_version."""
    from local_extensions import _check_version

    func = _check_version
    assert func(version, min_version, max_version) is expected


@pytest.mark.parametrize(
    "min_version,max_version,include_alphas,expected",
    (
        (14, None, False, "v16.13.1"),
        (14, 15, False, "v14.10.10"),
        (14, 15, True, "v14.10.10"),
        (None, None, True, "v16.14.0-alpha1"),
        (None, None, False, "v16.13.1"),
    ),
)
def test_latest_version(min_version, max_version, include_alphas, expected):
    """Test local_extensions.latest_version."""
    from local_extensions import latest_version

    versions = ["v16.13.1", "v14.10.10", "v16.14.0-alpha1"]
    func = latest_version
    assert func(versions, min_version, max_version, include_alphas) == expected


def test_filter_use_alpha_versions_with_env_var(monkeypatch, filter_test):
    """Test local_extensions.use_alpha_versions."""
    monkeypatch.setenv("USE_VOLTO_ALPHA", "1")
    result = filter_test("use_alpha_versions", "No")
    assert result == "Yes"


def test_filter_use_alpha_versions_no_env_var(monkeypatch, filter_test):
    """Test local_extensions.use_alpha_versions."""
    monkeypatch.delenv("USE_VOLTO_ALPHA", raising=False)
    result = filter_test("use_alpha_versions", "No")
    assert result == "No"


@pytest.mark.parametrize(
    "use_alpha_versions,expected",
    (
        ("'No'", "17.6.1"),
        ("'Yes'", "18.0.0-alpha.4"),
    ),
)
def test_filter_latest_volto(
    mock_volto_versions_call, filter_test, use_alpha_versions, expected
):
    """Test local_extensions.latest_volto."""
    result = filter_test("latest_volto", use_alpha_versions)
    assert result == expected


@pytest.mark.parametrize(
    "volto_version,expected",
    (
        ("'16.4.0'", "7.0.1"),
        ("'17.6.1'", "8.1.0"),
        ("'18.0.0-alpha.4'", "9.0.0-alpha.1"),
    ),
)
def test_filter_latest_volto_generator(
    mock_volto_generator_versions_call, filter_test, volto_version, expected
):
    """Test local_extensions.latest_volto_generator."""
    result = filter_test("latest_volto_generator", volto_version)
    assert result == expected


def test_filter_latest_plone(mock_plone_version_call, filter_test):
    """Test local_extensions.latest_plone."""
    result = filter_test("latest_plone", "6.0.8")
    assert result == "6.0.8"


@pytest.mark.parametrize(
    "volto_version,expected",
    (
        ("'16.4.0'", "16"),
        ("'17.6.1'", "18"),
        ("'18.0.0-alpha.4'", "20"),
    ),
)
def test_filter_node_version(filter_test, volto_version, expected):
    """Test local_extensions.node_version."""
    result = filter_test("node_version", volto_version)
    assert result == expected


@pytest.mark.parametrize(
    "code,expected",
    (
        ("'en'", "en"),
        ("'es'", "es"),
        ("'pt-br'", "pt-br"),
    ),
)
def test_filter_gs_language_code(filter_test, code, expected):
    """Test local_extensions.gs_language_code."""
    result = filter_test("gs_language_code", code)
    assert result == expected


@pytest.mark.parametrize(
    "code,expected",
    (
        ("'en'", "en"),
        ("'es'", "es"),
        ("'pt-br'", "pt_BR"),
    ),
)
def test_filter_locales_language_code(filter_test, code, expected):
    """Test local_extensions.locales_language_code."""
    result = filter_test("locales_language_code", code)
    assert result == expected


@pytest.mark.parametrize(
    "registry,expected",
    (
        ("'Docker Hub'", ""),
        ("'GitHub'", "ghcr.io/"),
    ),
)
def test_filter_docker_image_prefix(filter_test, registry, expected):
    """Test local_extensions.docker_image_prefix."""
    result = filter_test("docker_image_prefix", registry)
    assert result == expected


@pytest.mark.parametrize(
    "value,expected",
    (
        ("'plone_org'", "PloneOrg"),
        ("'plone_conf'", "PloneConf"),
        ("'ploneconf'", "Ploneconf"),
    ),
)
def test_filter_pascal_case(filter_test, value, expected):
    """Test local_extensions.pascal_case."""
    result = filter_test("pascal_case", value)
    assert result == expected


@pytest.mark.parametrize(
    "value,expected",
    (
        ("'plone.org'", "plone"),
        ("'plone.org.br'", "plone"),
        ("'site.com.br'", "site"),
    ),
)
def test_filter_extract_host(filter_test, value, expected):
    """Test local_extensions.extract_host."""
    result = filter_test("extract_host", value)
    assert result == expected
