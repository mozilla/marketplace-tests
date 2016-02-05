# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.desktop.consumer_pages.home import Home
from pages.desktop.consumer_pages.account_settings import My_Apps
from pages.desktop.consumer_pages.account_settings import AccountSettings
from pages.desktop.consumer_pages.account_settings import BasicInfo
from tests.base_test import BaseTest


class TestAccounts(BaseTest):

    def test_create_new_user_using_fxapom(self, base_url, selenium, new_user):
        home_page = Home(base_url, selenium)
        home_page.go_to_homepage()
        home_page.header.click_sign_in()
        home_page.login(new_user['email'], new_user['password'])
        assert not home_page.header.is_sign_in_visible
        assert home_page.is_the_current_page

        home_page.header.open_settings_menu()
        assert home_page.header.is_user_logged_in

    @pytest.mark.sanity
    @pytest.mark.nondestructive
    def test_user_can_sign_in_and_sign_out_from_home_page(self, base_url, selenium, new_user):
        home_page = Home(base_url, selenium)
        home_page.go_to_homepage()
        home_page.header.click_sign_in()
        home_page.login(new_user['email'], new_user['password'])
        assert home_page.is_the_current_page
        assert home_page.header.is_user_logged_in

        home_page.header.click_sign_out()
        assert home_page.header.is_sign_in_visible

    @pytest.mark.nondestructive
    def test_user_can_sign_in_and_sign_out_from_my_apps(self, base_url, selenium, new_user):
        my_apps_page = My_Apps(base_url, selenium)
        my_apps_page.go_to_my_apps_page()
        my_apps_page.click_sign_in()
        my_apps_page.login(new_user['email'], new_user['password'])
        assert my_apps_page.header.is_user_logged_in
        assert not my_apps_page.header.is_sign_in_visible

        my_apps_page.header.click_sign_out()
        assert my_apps_page.header.is_sign_in_visible

    @pytest.mark.nondestructive
    def test_user_can_sign_in_and_sign_out_from_settings_page(self, base_url, selenium, new_user):
        settings_page = AccountSettings(base_url, selenium)
        settings_page.go_to_settings_page()
        settings_page.click_sign_in()
        settings_page.login(new_user['email'], new_user['password'])
        assert settings_page.header.is_user_logged_in
        assert not settings_page.header.is_sign_in_visible

        settings_page.header.click_sign_out()
        assert settings_page.header.is_sign_in_visible

    def test_editing_user_profile(self, base_url, selenium, new_user):
        home_page = Home(base_url, selenium)
        home_page.go_to_homepage()
        home_page.header.click_sign_in()
        home_page.login(new_user['email'], new_user['password'])
        profile_page = home_page.header.click_edit_account_settings()
        assert profile_page.email.split('@')[0] == profile_page.display_name

        name = 'Napoleon'
        profile_page.edit_display_name(name)
        profile_page.save_changes()
        profile_page.wait_for_notification('Your settings have been successfully saved')
        profile_page.refresh_page()
        assert name == profile_page.display_name

    @pytest.mark.nondestructive
    def test_recommended_tab_shows_up_only_if_checkbox_is_selected(self, base_url, selenium, new_user):
        basic_info = BasicInfo(base_url, selenium)
        basic_info.go_to_settings_page()
        basic_info.click_sign_in()
        basic_info.login(new_user['email'], new_user['password'])
        assert basic_info.is_recommendations_enabled
        assert basic_info.is_recommended_tab_visible

        basic_info.disable_recommendations()
        basic_info.save_changes()
        basic_info.wait_for_recommended_tab_not_visible()
        assert not basic_info.is_recommended_tab_visible
