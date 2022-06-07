from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing.zope import WSGI_SERVER_FIXTURE

import {{ cookiecutter.python_package_name }}


class {{ cookiecutter.__python_package_name_upper }}Layer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package={{ cookiecutter.python_package_name }})

    def setUpPloneSite(self, portal):
        applyProfile(portal, "{{ cookiecutter.python_package_name }}:default")
        applyProfile(portal, "{{ cookiecutter.python_package_name }}:initial")


{{ cookiecutter.__python_package_name_upper }}_FIXTURE = {{ cookiecutter.__python_package_name_upper }}Layer()


{{ cookiecutter.__python_package_name_upper }}_INTEGRATION_TESTING = IntegrationTesting(
    bases=({{ cookiecutter.__python_package_name_upper }}_FIXTURE,),
    name="{{ cookiecutter.__python_package_name_upper }}Layer:IntegrationTesting",
)


{{ cookiecutter.__python_package_name_upper }}_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=({{ cookiecutter.__python_package_name_upper }}_FIXTURE, WSGI_SERVER_FIXTURE),
    name="{{ cookiecutter.__python_package_name_upper }}Layer:FunctionalTesting",
)


{{ cookiecutter.__python_package_name_upper }}ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        {{ cookiecutter.__python_package_name_upper }}_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        WSGI_SERVER_FIXTURE,
    ),
    name="{{ cookiecutter.__python_package_name_upper }}Layer:AcceptanceTesting",
)
