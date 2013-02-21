#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from unittestzero import Assert

from mocks.mock_application import MockApplication
from mocks.marketplace_api import MarketplaceAPI
from pages.desktop.developer_hub.home import Home
from tests.desktop.base_test import BaseTest


class TestAPI(BaseTest):

    def test_assert_that_a_app_can_be_added_by_api(self, mozwebqa):
        mock_app = MockApplication()  # generate mock app
        mock_app.name = 'API %s' % mock_app.name

        # API
        mk_api = MarketplaceAPI(credentials=mozwebqa.credentials['api'])  # init API client

        mk_api.submit_app(mock_app)  # submit app

        app_status = mk_api.app_status(mock_app)  # get app data from API

        # Selenium
        dev_home = Home(mozwebqa)
        dev_home.go_to_developers_homepage()
        dev_home.login(user="default")

        dev_submissions = dev_home.header.click_my_submissions()

        dev_submissions.sorter.sort_by('created')
        apps = dev_submissions.submitted_apps

        app_names = []
        for app in apps:
            app_names.append(app.name)

        Assert.contains(app_status['name'], app_names)
