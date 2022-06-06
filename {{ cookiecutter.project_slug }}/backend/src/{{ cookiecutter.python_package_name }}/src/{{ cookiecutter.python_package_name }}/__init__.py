"""Init and utils."""
from zope.i18nmessageid import MessageFactory

import logging


_ = MessageFactory("{{ cookiecutter.python_package_name }}")

logger = logging.getLogger("{{ cookiecutter.python_package_name }}")
