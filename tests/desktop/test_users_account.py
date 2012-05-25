#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from pages.desktop.consumer_pages.home import Home
from pages.desktop.consumer_pages.paypal import PayPal


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

    def test_that_user_can_set_up_pre_approval_on_payment_settings_page(self, mozwebqa):
        """
        Test for Litmus 58172.
        https://litmus.mozilla.org/show_test.cgi?id=58172
        """

        # We have to first login to paypal developer to access the paypal sandbox
        developer_paypal_page = PayPal(mozwebqa)
        developer_paypal_page.go_to_page()
        developer_paypal_page.login_paypal(user="paypal")
        Assert.true(developer_paypal_page.is_user_logged_in)

        # Now we start to test the marketplace pages
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

        # logging in to paypal sandbox
        paypal_sandbox = payment_settings_page.click_set_up_pre_approval()
        paypal_sandbox.click_login_tab()
        paypal_sandbox.login_paypal_sandbox(user="sandbox")
        Assert.true(paypal_sandbox.is_user_logged_in)

        try:
            # From this point on we have set up the pre-approval and need to remove this option after we check it
            paypal_sandbox.click_approve_button()

            Assert.true(payment_settings_page.is_pre_approval_enabled)
            Assert.true(payment_settings_page.is_success_message_visible)

        except Exception as exception:
            Assert.fail(exception)

        finally:
            if payment_settings_page.is_remove_pre_approval_button_visible:
                payment_settings_page.click_remove_pre_approval()
            Assert.false(payment_settings_page.is_remove_pre_approval_button_visible)

    def test_that_user_can_remove_prepapproval_on_payment_settings_page(self, mozwebqa):
        # We have to first login to paypal developer to access the paypal sandbox
        developer_paypal_page = PayPal(mozwebqa)
        developer_paypal_page.go_to_page()
        developer_paypal_page.login_paypal(user="paypal")
        Assert.true(developer_paypal_page.is_user_logged_in)

        # Now we start to test the marketplace pages
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        home_page.login(user="remove_preapproval")

        Assert.true(home_page.is_the_current_page)
        Assert.true(home_page.footer.is_user_logged_in)

        # go to Payment Settings page
        settings_page = home_page.footer.click_account_settings()
        Assert.true(settings_page.is_the_current_page)

        payment_settings_page = settings_page.click_payment_menu()
        Assert.true(payment_settings_page.is_the_current_page)
        Assert.equal('Payment Settings', payment_settings_page.header_title)

        try:
            # verify that pre-approval is active
            Assert.true(payment_settings_page.is_remove_pre_approval_button_visible)

            # remove pre-approval
            payment_settings_page.click_remove_pre_approval()
            Assert.false(payment_settings_page.is_remove_pre_approval_button_visible)
            Assert.false(payment_settings_page.is_pre_approval_enabled)
            Assert.true(payment_settings_page.is_success_message_visible)

        except Exception as exception:
            Assert.fail(exception)

        finally:
            # restore the account to the initial state
            # logging in to paypal sandbox
            paypal_sandbox = payment_settings_page.click_set_up_pre_approval()
            paypal_sandbox.click_login_tab()
            paypal_sandbox.login_paypal_sandbox(user="sandbox")
            Assert.true(paypal_sandbox.is_user_logged_in)

            # From this point on we have set up the pre-approval and need to remove this option after we check it
            paypal_sandbox.click_approve_button()

            Assert.true(payment_settings_page.is_pre_approval_enabled)
            Assert.true(payment_settings_page.is_success_message_visible)
