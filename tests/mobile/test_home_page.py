#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from pages.mobile.home import Home


class TestHomepage():

    @pytest.mark.nondestructive
    def test_that_promo_module_not_present_on_mobile(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.true(home_page.is_promo_box_not_visible)

    @pytest.mark.nondestructive
    def test_that_verifies_categories_menu(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.true(home_page.is_nav_menu_visible)

        home_page.open_categories_menu()
        Assert.true(home_page.is_category_section_visible)
        Assert.greater(len(home_page.categories), 0)

    @pytest.mark.nondestructive
    def test_switch_between_new_and_popular_tab(self, mozwebqa):
        """
        Test to verify functionality for switch between New/Popular Tabs
        """
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.true(home_page.is_popular_category_tab_visible)
        Assert.true(home_page.is_new_category_tab_visible)

        home_page.click_new_menu_tab()
        Assert.equal('New', home_page.feed_title_text)
        Assert.true(len(home_page.new_apps) > 0)

        home_page.click_popular_menu_tab()
        Assert.equal('Popular', home_page.feed_title_text)
        Assert.true(len(home_page.popular_apps) > 0)
