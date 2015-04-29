#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from pages.desktop.consumer_pages.home import Home
from pages.desktop.consumer_pages.account_settings import My_Apps
from pages.desktop.consumer_pages.account_settings import AccountSettings
from tests.base_test import BaseTest


class TestAccounts(BaseTest):

    @pytest.mark.credentials
    def test_create_new_user_using_API(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        home_page.header.click_sign_in()
        acct = self.create_new_user(mozwebqa)
        home_page.login(acct)

        Assert.false(home_page.header.is_sign_in_visible)
        Assert.true(home_page.is_the_current_page)

        home_page.header.open_settings_menu()
        Assert.true(home_page.header.is_user_logged_in)

    @pytest.mark.sanity
    @pytest.mark.credentials
    @pytest.mark.nondestructive
    def test_user_can_sign_in_and_sign_out_from_home_page(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        home_page.header.click_sign_in()
        acct = self.create_new_user(mozwebqa)
        home_page.login(acct)
        Assert.true(home_page.is_the_current_page)

        # Verify that user is logged in
        Assert.true(home_page.header.is_user_logged_in)

        home_page.header.click_sign_out()
        Assert.true(home_page.header.is_sign_in_visible)

    @pytest.mark.credentials
    @pytest.mark.nondestructive
    def test_user_can_sign_in_and_sign_out_from_my_apps(self, mozwebqa):

        settings_page = My_Apps(mozwebqa)
        settings_page.go_to_my_apps_page()

        settings_page.click_sign_in()
        acct = self.create_new_user(mozwebqa)
        settings_page.login(acct)

        Assert.true(settings_page.header.is_user_logged_in)
        Assert.false(settings_page.header.is_sign_in_visible)

        settings_page.header.click_sign_out()
        Assert.true(settings_page.header.is_sign_in_visible)

    @pytest.mark.credentials
    @pytest.mark.nondestructive
    def test_user_can_sign_in_and_sign_out_from_settings_page(self, mozwebqa):

        settings_page = AccountSettings(mozwebqa)
        settings_page.go_to_settings_page()

        settings_page.click_sign_in()
        acct = self.create_new_user(mozwebqa)
        settings_page.login(acct)

        Assert.true(settings_page.header.is_user_logged_in)
        Assert.false(settings_page.header.is_sign_in_visible)

        settings_page.click_sign_out()
        Assert.true(settings_page.header.is_sign_in_visible)

    @pytest.mark.credentials
    def test_editing_user_profile(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        home_page.header.click_sign_in()
        acct = self.create_new_user(mozwebqa)
        home_page.login(acct)

        profile_page = home_page.header.click_edit_account_settings()

        # Initial check
        Assert.equal(profile_page.email.split('@')[0], profile_page.display_name)

        # Data to submit
        name = 'Napoleon'

        profile_page.edit_display_name(name)
        profile_page.save_changes()
        profile_page.wait_for_notification('Your settings have been successfully saved')

        # Refresh page and then inspect saved settings
        profile_page.refresh_page()
        Assert.equal(profile_page.display_name, name)

    @pytest.mark.credentials
    def test_that_checks_changing_language(self, mozwebqa):

        if mozwebqa.base_url == 'https://marketplace-dev.allizom.org' or mozwebqa.base_url == 'https://marketplace.allizom.org':
            pytest.skip("We currently don't have the option for changing the language in Fireplace")

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        acct = self.create_new_user(mozwebqa)
        home_page.login(acct)

        profile_page = home_page.header.click_edit_account_settings()

        language = 'fr'

        before_lang_change = [profile_page.get_url_current_page(),
                              profile_page.page_title,
                              profile_page.account_settings_header_text,
                              profile_page.display_name_field_text,
                              profile_page.language_field_text,
                              profile_page.region_field_text,
                              profile_page.header.search_field_placeholder,
                              profile_page.save_button_text]

        profile_page.edit_language(language)
        profile_page.save_changes()

        after_lang_change = [profile_page.get_url_current_page(),
                             profile_page.page_title,
                             profile_page.account_settings_header_text,
                             profile_page.display_name_field_text,
                             profile_page.language_field_text,
                             profile_page.region_field_text,
                             profile_page.header.search_field_placeholder,
                             profile_page.save_button_text]

        Assert.not_equal(before_lang_change, after_lang_change)
