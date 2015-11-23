#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.mobile.home import Home
from tests.base_test import BaseTest


class TestAccounts(BaseTest):

    @pytest.mark.nondestructive
    def test_user_can_login_and_logout(self, mozwebqa, new_user):
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        home_page.more_menu.click_sign_in()
        home_page.login(new_user['email'], new_user['password'])
        settings_page = home_page.more_menu.click_settings()
        assert new_user['email'] == settings_page.email_text
        home_page = settings_page.more_menu.click_sign_out()
        assert home_page.is_sign_in_visible

    @pytest.mark.nondestructive
    def test_user_can_go_back_from_settings_page(self, mozwebqa, new_user):
        """
        https://bugzilla.mozilla.org/show_bug.cgi?id=795185#c11
        """
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        home_page.more_menu.click_sign_in()
        home_page.login(new_user['email'], new_user['password'])
        settings_page = home_page.more_menu.click_settings()
        assert new_user['email'] == settings_page.email_text

        home_page = settings_page.header.click_marketplace_icon()
        assert home_page.is_the_current_page
