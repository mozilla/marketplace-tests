#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from pages.desktop.consumer_pages.home import Home
from pages.desktop.consumer_pages.account_settings import My_Apps
from pages.desktop.consumer_pages.account_settings import AccountSettings
from pages.desktop.consumer_pages.account_settings import  BasicInfo
from tests.base_test import BaseTest


class TestAccounts(BaseTest):

    def test_create_new_user_using_fxapom(self, mozwebqa, new_user):
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        home_page.header.click_sign_in()
        home_page.login(new_user['email'], new_user['password'])

        Assert.false(home_page.header.is_sign_in_visible)
        Assert.true(home_page.is_the_current_page)

        home_page.header.open_settings_menu()
        Assert.true(home_page.header.is_user_logged_in)

    @pytest.mark.sanity
    @pytest.mark.nondestructive
    def test_user_can_sign_in_and_sign_out_from_home_page(self, mozwebqa, new_user):
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        home_page.header.click_sign_in()
        home_page.login(new_user['email'], new_user['password'])
        Assert.true(home_page.is_the_current_page)

        # Verify that user is logged in
        Assert.true(home_page.header.is_user_logged_in)

        home_page.header.click_sign_out()
        Assert.true(home_page.header.is_sign_in_visible)

    @pytest.mark.nondestructive
    def test_user_can_sign_in_and_sign_out_from_my_apps(self, mozwebqa, new_user):
        my_apps_page = My_Apps(mozwebqa)
        my_apps_page.go_to_my_apps_page()

        my_apps_page.click_sign_in()
        my_apps_page.login(new_user['email'], new_user['password'])

        Assert.true(my_apps_page.header.is_user_logged_in)
        Assert.false(my_apps_page.header.is_sign_in_visible)

        my_apps_page.header.click_sign_out()
        Assert.true(my_apps_page.header.is_sign_in_visible)

    @pytest.mark.nondestructive
    def test_user_can_sign_in_and_sign_out_from_settings_page(self, mozwebqa, new_user):
        settings_page = AccountSettings(mozwebqa)
        settings_page.go_to_settings_page()

        settings_page.click_sign_in()
        settings_page.login(new_user['email'], new_user['password'])

        Assert.true(settings_page.header.is_user_logged_in)
        Assert.false(settings_page.header.is_sign_in_visible)

        settings_page.click_sign_out()
        Assert.true(settings_page.header.is_sign_in_visible)

    def test_editing_user_profile(self, mozwebqa, new_user):
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        home_page.header.click_sign_in()
        home_page.login(new_user['email'], new_user['password'])

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

    @pytest.mark.nondestructive
    def test_recommended_tab_shows_up_only_if_checkbox_is_selected(self, mozwebqa, new_user):
        basic_info = BasicInfo(mozwebqa)
        basic_info.go_to_settings_page()

        basic_info.click_sign_in()
        basic_info.login(new_user['email'], new_user['password'])

        if basic_info.is_enable_recommendations_selected == False:
            basic_info.click_enable_recommendations_button()
            basic_info.save_changes()

        Assert.equal(basic_info.is_recommended_tab_visible, True)

        basic_info.click_enable_recommendations_button()
        basic_info.save_changes()

        Assert.equal(basic_info.is_recommended_tab_visible, False)
