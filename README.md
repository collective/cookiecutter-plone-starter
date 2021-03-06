[![Cookiecutter Plone Project CI](https://github.com/collective/cookiecutter-plone-starter/actions/workflows/ci.yml/badge.svg)](https://github.com/collective/cookiecutter-plone-starter/actions/workflows/ci.yml)
[![Built with Cookiecutter](https://img.shields.io/badge/built%20with-Cookiecutter-ff69b4.svg?logo=cookiecutter)](https://github.com/collective/cookiecutter-plone-starter/)
![GitHub](https://img.shields.io/github/license/collective/cookiecutter-plone-starter)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# Cookiecutter Plone Starter

Powered by [Cookiecutter](https://github.com/cookiecutter/cookiecutter), [Cookiecutter Plone Starter](https://github.com/collective/cookiecutter-plone-starter/) is a framework for jumpstarting [Plone](https://plone.org/) 6 projects quickly.

This framework relies on [volto-generator](https://github.com/plone/volto/tree/master/packages/generator-volto) to generate the frontend code that will be used.

## Features

- For Plone 6
- Works with Python 3.9

## Requirements

### Cookiecutter

Install `cookiecutter` command line:

```shell
pip install cookiecutter
```

### NodeJS & Yarn

First install `nvm` and latest `NodeJS` according to the [Plone documentation](https://6.dev-docs.plone.org/volto/getting-started/install.html#install-nvm-nodejs-version-manager).

After that, install `yarn` according to the [Plone documentation](https://6.dev-docs.plone.org/volto/getting-started/install.html#yarn-nodejs-package-manager)

### Docker

Install `Docker` according to the [official documentation](https://docs.docker.com/get-docker/).


## Usage

Generate a new Project using this:

```shell
cookiecutter gh:collective/cookiecutter-plone-starter
```

## Project Generation Options

These are all the template options that will be prompted by the [Cookiecutter CLI](https://github.com/cookiecutter/cookiecutter) prior to generating your project.

| Option | Description | Example |
| --- | --- | --- |
| `project_title` | Your project's human-readable name, capitals and spaces allowed. | **Plone Site** |
| `project_slug` | Your project's slug without spaces. Used to name your repository and Docker images. | **plone-site** |
| `description` | Describes your project and gets used in places like ``README.md`` and such. | **New site for our company.** |
| `author` | This is you! The value goes into places like ``LICENSE``, ``setup.py`` and such. | **Our Company** |
| `email` | The email address you want to identify yourself in the project. | **email@example.com** |
| `python_package_name` | Name of the Python package used to configure your project. It needs to be Python-importable, so no dashes, spaces or special characters are allowed. | **plone_site** |
| `plone_version` | Plone version to be used. This queries for the latest available Plone 6 version and presents it to you as the default value. | **6.0.0a4** |
| `volto_version` | Volto (Plone Frontend) version to be used. This queries for the latest available stable Volto version and presents it to you as the default value. | **16.0.0-alpha.8** |
| `language_code` | Language to be used on the site. | **pt-br** |
| `github_organization` | Used for GitHub and Docker repositories. | **collective**|
| `container_registry` | Container registry to be used. | **Docker Hub**|

## License

This project is licensed under the terms of the [MIT License](/LICENSE)
