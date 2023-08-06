from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer

import collective.abovecontenttitleportlets


class CollectiveAboveContentTitlePortletsLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.abovecontenttitleportlets)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.abovecontenttitleportlets:default")


COLLECTIVE_ABOVE_CONTENT_PORTLETS_FIXTURE = CollectiveAboveContentTitlePortletsLayer()


COLLECTIVE_ABOVE_CONTENT_PORTLETS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_ABOVE_CONTENT_PORTLETS_FIXTURE,),
    name="CollectiveAboveContentTitlePortletsLayer:IntegrationTesting",
)


COLLECTIVE_ABOVE_CONTENT_PORTLETS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_ABOVE_CONTENT_PORTLETS_FIXTURE,),
    name="CollectiveAboveContentTitlePortletsLayer:FunctionalTesting",
)
