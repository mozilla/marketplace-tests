#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from pages.desktop.consumer_pages.home import Home
from tests.desktop.base_test import BaseTest


class TestAccounts(BaseTest):

    @pytest.mark.credentials
    @pytest.mark.xfail(reason='Need to find a way to create a new account with Fxa')
    def test_create_new_user(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        home_page.login()
        Assert.false(home_page.header.is_sign_in_visible)
        Assert.true(home_page.is_the_current_page)

        home_page.header.hover_over_settings_menu()
        Assert.true(home_page.header.is_user_logged_in)

    @pytest.mark.credentials
    @pytest.mark.nondestructive
    def test_user_can_sign_in_and_sign_out_in_consumer_pages(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        home_page.login(user="default")

        Assert.true(home_page.is_the_current_page)

        # Verify that user is loggedin
        Assert.true(home_page.header.is_user_logged_in)

        home_page.header.click_sign_out()
        Assert.true(home_page.header.is_sign_in_visible)

    @pytest.mark.credentials
    def test_editing_user_profile(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        home_page.login(user="default")

        profile_page = home_page.header.click_edit_account_settings()
        initial_value = profile_page.display_name

        # Initial check
        Assert.equal(profile_page.email.split('@')[0], profile_page.display_name)

        # Data to submit
        name = 'Napoleon'

        profile_page.edit_display_name(name)
        profile_page.save_changes()
        profile_page.wait_notification_box_visible()
        Assert.true(profile_page.notification_visible)

        # Refresh page and then inspect saved settings
        profile_page.refresh_page()
        Assert.equal(profile_page.display_name, name)

        # Undo the changes
        profile_page.edit_display_name(initial_value)
        profile_page.save_changes()
        profile_page.wait_notification_box_visible()

    @pytest.mark.credentials
    def test_that_checks_changing_language(self, mozwebqa):

        if mozwebqa.base_url == 'https://marketplace-dev.allizom.org' or mozwebqa.base_url == 'https://marketplace.allizom.org':
            pytest.skip("We currently don't have the option for changing the language in Fireplace")

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        home_page.login()

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
