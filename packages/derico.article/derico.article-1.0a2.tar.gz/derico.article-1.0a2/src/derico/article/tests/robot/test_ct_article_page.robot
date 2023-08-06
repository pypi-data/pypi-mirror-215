# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s derico.article -t test_article_page.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src derico.article.testing.DERICO_ARTICLE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/derico/article/tests/robot/test_article_page.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a ArticlePage
  Given a logged-in site administrator
    and an add ArticlePage form
   When I type 'My ArticlePage' into the title field
    and I submit the form
   Then a ArticlePage with the title 'My ArticlePage' has been created

Scenario: As a site administrator I can view a ArticlePage
  Given a logged-in site administrator
    and a ArticlePage 'My ArticlePage'
   When I go to the ArticlePage view
   Then I can see the ArticlePage title 'My ArticlePage'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add ArticlePage form
  Go To  ${PLONE_URL}/++add++ArticlePage

a ArticlePage 'My ArticlePage'
  Create content  type=ArticlePage  id=my-article_page  title=My ArticlePage

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the ArticlePage view
  Go To  ${PLONE_URL}/my-article_page
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a ArticlePage with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the ArticlePage title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
