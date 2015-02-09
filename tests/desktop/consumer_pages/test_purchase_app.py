#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest
from unittestzero import Assert

from pages.desktop.consumer_pages.home import Home
from tests.base_test import BaseTest


class TestPurchaseApp(BaseTest):

    _app_name = 'Test Zippy With Me'
    PIN = '1234'

    @pytest.mark.credentials
    def test_that_user_can_purchases_an_app(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        acct = self.create_new_user(mozwebqa)
        home_page.header.click_sign_in()
        home_page.login(acct)
        Assert.true(home_page.is_the_current_page)
        home_page.set_region("restofworld")

        details_page = home_page.header.search_and_click_on_app(self._app_name)
        Assert.not_equal("Free", details_page.price_text)
        Assert.true('paid' in details_page.app_status)

        payment = details_page.click_install_button()
        payment.create_pin(self.PIN)
        payment.wait_for_buy_app_section_displayed()
        Assert.equal(self._app_name, payment.app_name)

        payment.click_buy_button()
        Assert.false('paid' in details_page.app_status)
        Assert.equal('Install', payment.price_text)
