#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from pages.desktop.consumer_pages.home import Home


class TestAccounts:

    @pytest.mark.nondestructive
    def test_user_can_login_and_logout_using_browser_id_in_consumer_pages(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        home_page.login()

        Assert.true(home_page.is_the_current_page)
        Assert.true(home_page.footer.is_user_logged_in)

        home_page.footer.click_logout()
        Assert.false(home_page.footer.is_user_logged_in)

    @pytest.mark.xfail(reason="fix PayPalSandbox.click_login_tab")
    def test_that_user_can_set_up_pre_approval_on_payment_settings_page(self, mozwebqa):
        """
        Test for Litmus 58172.
        https://litmus.mozilla.org/show_test.cgi?id=58172
        """
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        home_page.login()

        Assert.true(home_page.is_the_current_page)
        Assert.true(home_page.footer.is_user_logged_in)

        # go to Payment Settings page
        settings_page = home_page.footer.click_account_settings()
        Assert.true(settings_page.is_the_current_page)

        payment_settings_page = settings_page.click_payment_menu()
        Assert.equal('Payment Settings', payment_settings_page.header_title)

        # User is redirected to the PayPal website to login to his account.
        paypal_sandbox = payment_settings_page.click_set_up_pre_approval()
        Assert.true(paypal_sandbox.is_the_current_page)

        paypal = paypal_sandbox.click_login_link()
        Assert.true(paypal.is_the_current_page)

        paypal.login_paypal(user="paypal")
        Assert.true(paypal.is_user_logged_in)

        # return to Payment Settings page and set pre-approval
        payment_settings_page.go_to_payment()
        Assert.equal('Payment Settings', payment_settings_page.header_title)

        try:
            paypal_sandbox = payment_settings_page.click_set_up_pre_approval()
            paypal_sandbox.click_login_tab()
            paypal_sandbox.login_paypal_sandbox(user="sandbox")
            Assert.true(paypal_sandbox.is_user_logged_in)
            paypal_sandbox.click_approve_button()

            Assert.true(payment_settings_page.is_pre_approval_successful)
            Assert.equal("Your payment pre-approval is enabled.", payment_settings_page.pre_approval_enabled)

        except Exception as exception:
            Assert.fail(exception.msg)

        finally:
            if (payment_settings_page.is_remove_pre_approval_button_visible):
                payment_settings_page.click_remove_pre_approval()
