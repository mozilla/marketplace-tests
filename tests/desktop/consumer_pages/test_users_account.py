#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from persona_test_user import PersonaTestUser
from pages.desktop.consumer_pages.home import Home
from tests.desktop.base_test import BaseTest


class TestAccounts(BaseTest):

    def test_create_new_user(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        home_page.login()
        Assert.true(home_page.footer.is_signed_in_notification_visible)
        Assert.true(home_page.is_the_current_page)

        home_page.header.hover_over_settings_menu()
        Assert.true(home_page.header.is_user_logged_in)

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

    def test_editing_user_profile(self, mozwebqa):
        """Test for https://www.pivotaltracker.com/story/show/33709085"""

        user = PersonaTestUser().create_user()

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        home_page.login(user)

        profile_page = home_page.header.click_account_settings()
        _username = user['email'].split('@')[0]

        # Initial check
        Assert.equal(profile_page.browser_id_email, user['email'])
        Assert.equal(profile_page.display_name, _username)

        # Data to submit. Username should be unique
        name = 'Napoleon'
        region = 'br'

        profile_page.edit_display_name(name)
        profile_page.edit_region(region)
        profile_page.save_changes()
        Assert.true(profile_page.is_notification_box_visible)

        # Refresh page and then inspect saved settings
        profile_page.refresh_page()

        Assert.equal(profile_page.display_name, name)
        Assert.equal(profile_page.change_user_region, region)

    def test_that_checks_changing_language(self, mozwebqa):
        """Test for https://www.pivotaltracker.com/story/show/33702365"""

        if mozwebqa.base_url == 'https://marketplace-dev.allizom.org' or mozwebqa.base_url == 'https://marketplace.allizom.org':
            pytest.skip("We currently don't have the option for changing the language in Fireplace")

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        home_page.login()

        profile_page = home_page.header.click_account_settings()

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
