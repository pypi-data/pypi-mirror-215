# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import derico.article


class DericoArticleLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=derico.article)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "derico.article:default")


DERICO_ARTICLE_FIXTURE = DericoArticleLayer()


DERICO_ARTICLE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(DERICO_ARTICLE_FIXTURE,),
    name="DericoArticleLayer:IntegrationTesting",
)


DERICO_ARTICLE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DERICO_ARTICLE_FIXTURE,),
    name="DericoArticleLayer:FunctionalTesting",
)


DERICO_ARTICLE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        DERICO_ARTICLE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="DericoArticleLayer:AcceptanceTesting",
)
