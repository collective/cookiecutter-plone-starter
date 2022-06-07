from AccessControl.SecurityManagement import newSecurityManager
from {{ cookiecutter.python_package_name }}.interfaces import I{{ cookiecutter.__python_package_name_upper }}Layer
from Products.CMFPlone.factory import _DEFAULT_PROFILE
from Products.CMFPlone.factory import addPloneSite
from Testing.makerequest import makerequest
from zope.interface import directlyProvidedBy
from zope.interface import directlyProvides

import os
import transaction


truthy = frozenset(("t", "true", "y", "yes", "on", "1"))


def asbool(s):
    """Return the boolean value ``True`` if the case-lowered value of string
    input ``s`` is a :term:`truthy string`. If ``s`` is already one of the
    boolean values ``True`` or ``False``, return it."""
    if s is None:
        return False
    if isinstance(s, bool):
        return s
    s = str(s).strip()
    return s.lower() in truthy


DELETE_EXISTING = asbool(os.getenv("DELETE_EXISTING"))

app = makerequest(app)  # noQA

request = app.REQUEST

ifaces = [
    I{{ cookiecutter.__python_package_name_upper }}Layer,
] + list(directlyProvidedBy(request))

directlyProvides(request, *ifaces)

admin = app.acl_users.getUserById("admin")
admin = admin.__of__(app.acl_users)
newSecurityManager(None, admin)

site_id = "Plone"
payload = {
    "title": "{{ cookiecutter.project_title }}",
    "profile_id": _DEFAULT_PROFILE,
    "extension_ids": [
        "{{ cookiecutter.python_package_name }}:default",
        "{{ cookiecutter.python_package_name }}:initial",
    ],
    "setup_content": False,
    "default_language": "{{ cookiecutter.__profile_language }}",
    "portal_timezone": "America/Sao_Paulo",
}

if site_id in app.objectIds() and DELETE_EXISTING:
    app.manage_delObjects([site_id])
    transaction.commit()
    app._p_jar.sync()

if site_id not in app.objectIds():
    site = addPloneSite(app, site_id, **payload)
    transaction.commit()
    app._p_jar.sync()
