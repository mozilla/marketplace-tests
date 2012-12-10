#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest

from unittestzero import Assert

from mocks.mock_application import MockApplication
from mocks.marketplace_app import MarketplaceApp
from pages.desktop.developer_hub.home import Home
from tests.desktop.base_test import BaseTest


class TestAPI(BaseTest):

    def test_assert_that_a_app_can_be_added_by_api(self, mozwebqa):
        mock_app = MockApplication() # generate mock app

        # API
        mk_app = MarketplaceApp(mock_app, user=mozwebqa.credentials['default']) # init API client

        mk_app.validate_manifest() # Validate manifest
        mk_app.submit_app() # submit app
        mk_app.update() # update app data
        mk_app.add_screenshot() # add screenshot
        mk_app.push_app_to_peeding_state_app()

        app_status = mk_app.get_app_status # get app data from API

        # Selenium
        dev_home = Home(mozwebqa)
        dev_home.go_to_developers_homepage()
        dev_home.login(user="default")

        dev_submissions = dev_home.header.click_my_submissions()

        dev_submissions.sorter.sort_by('created')
        apps = dev_submissions.submitted_apps

        app_names= []
        for app in apps:
            app_names.append(app.name)

        Assert.contains(app_status['name'],  app_names)

