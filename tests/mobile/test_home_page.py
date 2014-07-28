#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import pytest
from unittestzero import Assert

from pages.mobile.home import Home


class TestHomepage():

    def _restart(self, mozwebqa):
        os.popen("adb kill-server").read().strip()
        os.popen("adb start-server").read().strip()

    @pytest.mark.nondestructive
    def test_that_verifies_categories_section(self, mozwebqa):
        self._restart(mozwebqa)

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.true(home_page.is_featured_section_visible)
        Assert.true(home_page.is_gallery_section_visible)

        home_page.expand_all_categories_section()
        Assert.true(home_page.is_category_section_visible)
        Assert.greater(len(home_page.categories), 0)

    @pytest.mark.nondestructive
    def test_switch_between_new_and_popular_tab(self, mozwebqa):
        """
        Test to verify functionality for switch between New/Popular Tabs
        """
        self._restart(mozwebqa)

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.true(home_page.is_popular_category_tab_visible)
        Assert.true(home_page.is_new_category_tab_visible)
        Assert.true(home_page.is_popular_category_tab_selected)

        new_apps = home_page.click_new_category_tab()
        Assert.true(home_page.is_new_category_tab_selected)
        Assert.true(len(new_apps) > 0)
