#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest
from unittestzero import Assert

from pages.desktop.consumer_pages.home import Home
from tests.base_test import BaseTest


class TestPurchaseApp(BaseTest):

    PIN = '1234'

    @pytest.mark.credentials
    def test_that_user_can_purchase_an_app(self, mozwebqa):

        if '-dev' not in mozwebqa.base_url:
            pytest.skip("Payments can only be tested on dev.")

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        acct = self.create_new_user(mozwebqa)
        home_page.header.click_sign_in()
        home_page.login(acct)
        Assert.true(home_page.is_the_current_page)
        home_page.set_region('us')

        # Use the first paid app
        app = home_page.header.search(':paid').results[0]
        app_name = app.name
        details_page = app.click_name()
        Assert.false('free' in details_page.price_text)
        Assert.true('paid' in details_page.app_status)

        payment = details_page.click_install_button()
        payment.create_pin(self.PIN)
        payment.wait_for_buy_app_section_displayed()
        Assert.equal(app_name, payment.app_name)

        payment.click_buy_button()
        # We are not able to interact with the doorhanger that appears to install the app
        # using Selenium
        # We can check for the `purchased` attribute on the price button though
        details_page.wait_for_app_purchased()
