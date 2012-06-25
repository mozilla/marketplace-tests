#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from pages.desktop.consumer_pages.home import Home
from pages.desktop.paypal.paypal import PayPal
from mocks.mock_user import MockUser


class TestAccounts:

    def test_create_new_user(self, mozwebqa):
        user = MockUser()
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        home_page.create_new_user(user)

        Assert.true(home_page.is_the_current_page)
        Assert.true(home_page.footer.is_user_logged_in)

    @pytest.mark.nondestructive
    def test_user_can_login_and_logout_using_browser_id_in_consumer_pages(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        home_page.login(user="default")

        Assert.true(home_page.is_the_current_page)
        Assert.true(home_page.footer.is_user_logged_in)

        home_page.footer.click_logout()
        Assert.false(home_page.footer.is_user_logged_in)

    def test_that_user_can_set_up_pre_approval_on_payment_settings_page(self, mozwebqa):
        """
        Test for Litmus 58172.
        https://litmus.mozilla.org/show_test.cgi?id=58172
        """

        # We have to first log in to PayPal developer to access the PayPal sandbox
        self._developer_page_login_to_paypal(mozwebqa)

        # get to payment settings page as 'add_preapproval' user
        payment_settings_page = self._payment_settings_page_as_user(mozwebqa, 'add_preapproval')

        try:
            # set up non-pre-approval precondition
            if payment_settings_page.is_remove_pre_approval_button_visible:
                payment_settings_page.click_remove_pre_approval()
                Assert.false(payment_settings_page.is_remove_pre_approval_button_visible)

            # do test
            payment_settings_page = self._set_up_pre_approval(payment_settings_page)

            # verify
            Assert.true(payment_settings_page.is_pre_approval_enabled)
            Assert.true(payment_settings_page.is_success_message_visible)

        finally:
            # clean up
            if payment_settings_page.is_remove_pre_approval_button_visible:
                payment_settings_page.click_remove_pre_approval()
            Assert.false(payment_settings_page.is_remove_pre_approval_button_visible)

    @pytest.mark.xfail(reason="Test fails sporadically https://www.pivotaltracker.com/story/show/30992181")
    def test_that_user_can_remove_prepapproval_on_payment_settings_page(self, mozwebqa):
        # We have to first login to PayPal developer to access the PayPal sandbox
        self._developer_page_login_to_paypal(mozwebqa)

        # get to payment settings page as 'remove_preapproval' user
        payment_settings_page = self._payment_settings_page_as_user(mozwebqa, 'remove_preapproval')

        try:
            # set up pre-approval precondition
            if not payment_settings_page.is_pre_approval_enabled:
                payment_settings_page = self._set_up_pre_approval(payment_settings_page)
                Assert.true(payment_settings_page.is_remove_pre_approval_button_visible,
                    "Remove pre-approval button is not available. Pre-approval might be off")

            # do test
            payment_settings_page.click_remove_pre_approval()

            # verify
            Assert.false(payment_settings_page.is_remove_pre_approval_button_visible,
                "Remove pre-approval button is visible after click_remove_pre_approval")
            Assert.false(payment_settings_page.is_pre_approval_enabled, 
                "Pre-approval is still enabled")
            Assert.true(payment_settings_page.is_success_message_visible, 
                "Success message is not visible")

        finally:
            # restore the account to the initial state
            payment_settings_page = self._set_up_pre_approval(payment_settings_page)
            Assert.true(payment_settings_page.is_pre_approval_enabled)
            Assert.true(payment_settings_page.is_success_message_visible)

    def _developer_page_login_to_paypal(self, mozwebqa):
        developer_paypal_page = PayPal(mozwebqa)
        developer_paypal_page.go_to_page()
        developer_paypal_page.login_paypal(user="paypal")
        Assert.true(developer_paypal_page.is_user_logged_in)
        return developer_paypal_page

    def _payment_settings_page_as_user(self, mozwebqa, user):
        # Now we start to test the marketplace pages
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        home_page.login(user=user)

        Assert.true(home_page.is_the_current_page)
        Assert.true(home_page.footer.is_user_logged_in)

        # go to Payment Settings page
        settings_page = home_page.footer.click_account_settings()
        Assert.true(settings_page.is_the_current_page)

        payment_settings_page = settings_page.click_payment_menu()
        Assert.equal('Payment Settings', payment_settings_page.header_title)
        return payment_settings_page

    def _set_up_pre_approval(self, payment_settings_page):
        # request pre-approval
        paypal_sandbox = payment_settings_page.click_set_up_pre_approval()

        # login PayPal sandbox will throw a timeout error if login box doesn't appear
        paypal_sandbox.login_paypal_sandbox(user="sandbox")
        Assert.true(paypal_sandbox.is_user_logged_in)

        # enact preapproval
        payment_settings_page = paypal_sandbox.click_approve_button()

        return payment_settings_page
