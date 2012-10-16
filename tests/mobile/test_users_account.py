#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from pages.mobile.home import Home
from tests.mobile.base_test import BaseTest


class TestAccounts(BaseTest):

    @pytest.mark.nondestructive
    def test_user_can_login_and_logout(self, mozwebqa):
        self.clear_local_storage(mozwebqa)

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        home_page.login_with_user(user="default")
        home_page.wait_for_page_to_load()
        Assert.false(home_page.footer.is_login_visibile)

        Assert.true(home_page.is_the_current_body_class)
        settings_page = home_page.header.click_settings()

        Assert.equal(settings_page.email_text, mozwebqa.credentials["default"]["email"])

        home_page = settings_page.click_logout()
        Assert.true(home_page.is_the_current_body_class)
        Assert.true(home_page.footer.is_login_visibile)
