"""Installer for the {{ cookiecutter.python_package_name }} package."""
from setuptools import find_packages
from setuptools import setup


long_description = "\n\n".join(
    [
        open("README.md").read(),
        open("CONTRIBUTORS.md").read(),
        open("CHANGES.md").read(),
    ]
)


setup(
    name="{{ cookiecutter.python_package_name }}",
    version="1.0.0a1",
    description="{{ cookiecutter.project_title }} configuration package.",
    long_description=long_description,
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone CMS",
    author="{{ cookiecutter.author }}",
    author_email="{{ cookiecutter.email }}",
    url="https://github.com/{{ cookiecutter.github_organization }}/{{ cookiecutter.project_slug }}",
    project_urls={
        "PyPI": "https://pypi.python.org/pypi/{{ cookiecutter.python_package_name }}",
        "Source": "https://github.com/{{ cookiecutter.github_organization }}/{{ cookiecutter.project_slug }}",
        "Tracker": "https://github.com/{{ cookiecutter.github_organization }}/{{ cookiecutter.project_slug }}/issues",
    },
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=[
        "setuptools",
        "Plone",
        "prettyconf",
        "plone.api",
    ],
    extras_require={
        "test": [
            "parameterized",
            "zest.releaser[recommended]",
            "plone.app.testing[robot]>=7.0.0a3",
            "plone.restapi[test]",
            "collective.MockMailHost",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = {{ cookiecutter.python_package_name }}.locales.update:update_locale
    """,
)
