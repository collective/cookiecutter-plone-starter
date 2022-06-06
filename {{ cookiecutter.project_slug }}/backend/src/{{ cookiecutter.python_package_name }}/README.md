# {{ cookiecutter.python_package_name }}

{{ cookiecutter.description }}

## Features

### CORS settings

Implement CORS settings for this package

### Content types

- Training

### Initial content

This package contains a simple volto configuration.

Installation
------------

Install {{ cookiecutter.python_package_name }} by adding it to your buildout:
```ini
[buildout]

...

eggs =
    {{ cookiecutter.python_package_name }}
```

Then running `buildout`

And to create the Plone site:

```shell
./bin/instance run scripts/create_site.py
```

## Contribute

- [Issue Tracker](https://github.com/{{ cookiecutter.github_organization }}/{{ cookiecutter.project_slug }}/issues)
- [Source Code](https://github.com/{{ cookiecutter.github_organization }}/{{ cookiecutter.project_slug }}/)

## License

The project is licensed under the GPLv2.
