#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from pages.mobile.home import Home


class TestSettings():

    @pytest.mark.nondestructive
    def test_anonymous_user_can_change_region(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        settings_page = home_page.header.click_settings()
        settings_page.change_region('es')
        settings_page.save_changes()

        home_page.go_to_homepage()
        settings_page = home_page.header.click_settings()

        Assert.equal(settings_page.region, 'es')
