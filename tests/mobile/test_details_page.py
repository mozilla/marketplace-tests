#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from pages.mobile.home import Home


class TestDetails():

    @pytest.mark.nondestructive
    def test_details_page_for_an_app(self, mozwebqa):
        '''https://moztrap.mozilla.org/runtests/run/243/env/112/ - Verify details page for an app'''
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        #first app name
        first_featured_app_name = home_page.first_featured_app_name

        #click first app and load its Details Page
        details_page = home_page.click_first_featured_app()

        #The verifications required by the testcase
        Assert.true(first_featured_app_name in  details_page.title)
        Assert.true(details_page.header.is_back_button_visible)
        Assert.true(details_page.is_app_icon_present)
        Assert.true(details_page.is_product_details_visible)
        Assert.true(details_page.is_description_present)
