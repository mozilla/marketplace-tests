#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from mocks.mock_user import MockUser
from pages.desktop.consumer_pages.home import Home
from tests.desktop.base_test import BaseTest


class TestAccounts(BaseTest):

#    def test_create_new_user(self, mozwebqa):
#        user = MockUser()
#        home_page = Home(mozwebqa)
#        home_page.go_to_homepage()
#
#        home_page.create_new_user(user)
#        home_page.login(user)
#
#        Assert.true(home_page.is_the_current_page)
#        Assert.true(home_page.header.is_user_logged_in)

#    @pytest.mark.nondestructive
#    def test_user_can_sign_in_and_sign_out_using_browser_id_in_consumer_pages(self, mozwebqa):
#        home_page = Home(mozwebqa)
#        home_page.go_to_homepage()
#        home_page.login(user="default")
#
#        Assert.true(home_page.is_the_current_page)
#        home_page.header.hover_over_settings_menu()
#        Assert.true(home_page.header.is_user_logged_in)
#        home_page.header.hover_over_settings_menu()
#        home_page.header.click_sign_out()
#        Assert.false(home_page.header.is_user_logged_in)

#    def test_that_user_can_set_up_pre_approval_on_payment_settings_page(self, mozwebqa):
#        """
#        Test for Litmus 58172.
#        https://litmus.mozilla.org/show_test.cgi?id=58172
#        """
#
#        # We have to first log in to PayPal developer to access the PayPal sandbox
#        self._developer_page_login_to_paypal(mozwebqa)
#
#        # Login to consumer pages
#        home_page, user = self._login_to_consumer_pages(mozwebqa, 'add_preapproval')
#
#        # get to payment settings page
#        payment_settings_page = self._open_payment_settings_page(home_page)
#
#        try:
#            # set up non-pre-approval precondition
#            if payment_settings_page.is_remove_pre_approval_button_visible:
#                payment_settings_page.click_remove_pre_approval()
#                Assert.false(payment_settings_page.is_remove_pre_approval_button_visible)
#
#            # do test
#            payment_settings_page = self._set_up_pre_approval(payment_settings_page)
#
#            # verify
#            Assert.true(payment_settings_page.is_pre_approval_enabled)
#            Assert.true(payment_settings_page.is_success_message_visible)
#
#        finally:
#            # clean up
#            if payment_settings_page.is_remove_pre_approval_button_visible:
#                payment_settings_page.click_remove_pre_approval()
#            Assert.false(payment_settings_page.is_remove_pre_approval_button_visible)

#    def test_that_user_can_remove_prepapproval_on_payment_settings_page(self, mozwebqa):
#        # We have to first login to PayPal developer to access the PayPal sandbox
#        self._developer_page_login_to_paypal(mozwebqa)
#
#        # Login to consumer pages
#        home_page, user = self._login_to_consumer_pages(mozwebqa, 'remove_preapproval')
#
#        # get to payment settings page
#        payment_settings_page = self._open_payment_settings_page(home_page)
#
#        try:
#            # set up pre-approval precondition
#            if not payment_settings_page.is_pre_approval_enabled:
#                payment_settings_page = self._set_up_pre_approval(payment_settings_page)
#                Assert.true(payment_settings_page.is_remove_pre_approval_button_visible,
#                    "Remove pre-approval button is not available. Pre-approval might be off")
#
#            # do test
#            payment_settings_page.click_remove_pre_approval()
#
#            # verify
#            Assert.false(payment_settings_page.is_remove_pre_approval_button_visible,
#                "Remove pre-approval button is visible after click_remove_pre_approval")
#            Assert.false(payment_settings_page.is_pre_approval_enabled,
#                "Pre-approval is still enabled")
#            Assert.true(payment_settings_page.is_success_message_visible,
#                "Success message is not visible")
#
#        finally:
#            # restore the account to the initial state
#            payment_settings_page = self._set_up_pre_approval(payment_settings_page)
#            Assert.true(payment_settings_page.is_pre_approval_enabled)
#            Assert.true(payment_settings_page.is_success_message_visible)

    @pytest.mark.nondestructive
    def test_editing_user_profile(self, mozwebqa):
        """Test for https://www.pivotaltracker.com/story/show/33709085"""
        
        user = MockUser()
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        home_page.create_new_user(user)
        home_page.login(user)

        self.hover_over_settings_menu()
        profile_page = home_page.header.click_account_settings()
        _username = user['email'].split('@')[0]

        #Initial check
        Assert.equal(profile_page.browser_id_email, user['email'])
        Assert.equal(profile_page.username, _username)
        Assert.equal(profile_page.display_name, _username)

        #Data to submit. Username and Bio should be unique 
        name = 'Napoleon'
        username = _username[::-1]
        region = 'Saint Helena'

        profile_page.edit_display_name(name)
        profile_page.edit_username(username)
        profile_page.edit_region(region)
#        profile_page.edit_occupation(occupation)
#        profile_page.edit_homepage(homepage)
#        profile_page.edit_bio(bio)
#        profile_page.check_email_me_checkbox()
        profile_page.save_changes()

        Assert.equal(profile_page.display_name, name)
        Assert.equal(profile_page.username, username)
        Assert.equal(profile_page.region, region)
