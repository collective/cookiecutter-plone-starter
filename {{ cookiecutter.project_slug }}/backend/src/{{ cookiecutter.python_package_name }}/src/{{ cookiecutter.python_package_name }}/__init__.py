"""Init and utils."""
from zope.i18nmessageid import MessageFactory

import logging


PACKAGE_NAME = "{{ cookiecutter.python_package_name }}"

_ = MessageFactory("{{ cookiecutter.python_package_name }}")

logger = logging.getLogger("{{ cookiecutter.python_package_name }}")
