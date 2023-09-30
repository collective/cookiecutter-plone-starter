# Cookiecutter Plone Starter 🌟

[![Cookiecutter Plone Project CI](https://github.com/collective/cookiecutter-plone-starter/actions/workflows/ci.yml/badge.svg)](https://github.com/collective/cookiecutter-plone-starter/actions/workflows/ci.yml)
[![Built with Cookiecutter](https://img.shields.io/badge/built%20with-Cookiecutter-ff69b4.svg?logo=cookiecutter)](https://github.com/collective/cookiecutter-plone-starter/)
![GitHub](https://img.shields.io/github/license/collective/cookiecutter-plone-starter)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Welcome to **Cookiecutter Plone Starter**! Your one-stop solution to kickstart [Plone](https://plone.org/) 6 projects with ease and efficiency. Powered by [Cookiecutter](https://github.com/cookiecutter/cookiecutter), this template is designed to save you time and ensure that you get started on the right foot. 🚀

## Features ✨

- Tailored for Plone 6
- Compatible with Python 3.8, 3.9, 3.10, 3.11
- Leverages [volto-generator](https://github.com/plone/volto/tree/master/packages/generator-volto) for frontend code generation

## Getting Started 🏁

### Prerequisites

- **pipx**: A handy tool for installing and running Python applications.
- **NodeJS & Yarn**: Essential for managing and running JavaScript packages.
- **Docker**: For containerization and easy deployment.

### Installation Guide 🛠️

1. **pipx**

```shell
pip install pipx
```

2. **NodeJS & Yarn**

Follow the [Plone documentation](https://6.docs.plone.org/volto/getting-started/install.html) for detailed instructions.

3. **Docker**

Visit the [official documentation](https://docs.docker.com/get-docker/) for installation guides.

### Generate Your Plone 6 Project 🎉

```shell
pipx run cookiecutter gh:collective/cookiecutter-plone-starter
```

For alpha versions of Volto:

```shell
USE_VOLTO_ALPHA=1 pipx run cookiecutter gh:collective/cookiecutter-plone-starter
```

### Initial Build

```shell
make install
```

### Start Servers

Backend:

```shell
make start-backend
```

Frontend:

```shell
make start-frontend
```

### Rebuild After Changes

```shell
make build
make start-backend
make start-frontend
```

## Project Generation Options 🛠️

Every project is unique, and we provide a variety of options to ensure that your Plone 6 project aligns with your specific needs. Here are the options you can customize during the generation process:

| Option                | Description                                                                                                                                          | Example                       |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| `project_title`       | Your project's human-readable name, capitals and spaces allowed.                                                                                     | **Plone Site**                |
| `description`         | Describes your project and gets used in places like ``README.md`` and such.                                                                          | **New site for our company.** |
| `project_slug`        | Your project's slug without spaces. Used to name your repository and Docker images.                                                                  | **plone-site**                |
| `hostname`            | Hostname where the project will be deployed.                                                                                                         | **site.plone.org**            |
| `author`              | This is you! The value goes into places like ``LICENSE``, ``setup.py`` and such.                                                                     | **Our Company**               |
| `email`               | The email address you want to identify yourself in the project.                                                                                      | **email@example.com**         |
| `python_package_name` | Name of the Python package used to configure your project. It needs to be Python-importable, so no dashes, spaces or special characters are allowed. | **plone_site**                |
| `volto_addon_name`    | Name of the Volto addon package used to configure your frontend project. No spaces or special characters are allowed.                                | **volto-plone-site**          |
| `python_test_framework` | Select which Python testing framework to use in the project                                                                                        | **pytest**                    |
| `plone_version`       | Plone version to be used. This queries for the latest available Plone 6 version and presents it to you as the default value.                         | **6.0.0**                     |
| `use_alpha_versions`  | Use non-stable versions of Volto, (The default value could also be set via `USE_VOLTO_ALPHA` environment variable.                                   | **Yes**                       |
| `volto_version`       | Volto (Plone Frontend) version to be used. This queries for the latest available Volto version and presents it to you as the default value.          | **16.4.1**                    |
| `volto_generator_version`       | Volto (Plone Frontend) Yeoman generator to be used. This queries for the latest available Volto Generator version and presents it to you as the default value. Non-stable versions will be included if a non-stable version was selected for `volto_version`.   | **6.0.0**                    |
| `language_code`       | Language to be used on the site.                                                                                                                     | **pt-br**                     |
| `github_organization` | Used for GitHub and Docker repositories.                                                                                                             | **collective**                |
| `container_registry`  | Container registry to be used.                                                                                                                       | **GitHub**                    |
| `devops_ansible`      | Should we create an Ansible playbook to bootstrap and deploy this project?                                                                           | **Yes**                       |
| `devops_gha_deploy`   | Should we create a GitHub action to deploy this project?                                                                                             | **Yes**                       |


## Dive into Your Project's Structure 🏗️

Your generated project will have a well-organized structure, ensuring that both development and maintenance are a breeze. It includes separate sections for backend, frontend, and devops, each tailored for its specific role.

(Include the Structure and Reasoning section from the previous README.md here, as it provides a good overview of the project structure)

## Code Quality Assurance 🧐

Your project comes equipped with linters to ensure code quality. Run the following to automatically format your code:

```shell
make format
```

## Internationalization 🌐

Generate translation files with ease:

```shell
make i18n
```

## License 📜

This project is licensed under the [MIT License](/LICENSE).

## Let's Get Building! 🚀

Happy coding!
