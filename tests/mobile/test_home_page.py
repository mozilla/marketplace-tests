#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from pages.mobile.home import Home


class TestHomepage():

    @pytest.mark.nondestructive
    def test_that_verifies_categories_section(self, mozwebqa):

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
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.true(home_page.is_popular_category_tab_visible)
        Assert.true(home_page.is_new_category_tab_visible)
        Assert.true(home_page.is_popular_category_tab_selected)

        new_apps = home_page.click_new_category_tab()
        Assert.true(home_page.is_new_category_tab_selected)
        Assert.true(len(new_apps) > 0)

    @pytest.mark.nondestructive
    def test_view_all_link_in_popular_new_tab(self, mozwebqa):
        """
        Test to verify the 'View All' link in the New/Popular section
        """
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.true(home_page.is_popular_category_tab_visible)
        Assert.true(home_page.is_new_category_tab_visible)

        Assert.true(home_page.is_popular_category_tab_selected)
        popular_apps_search_page = home_page.click_new_popular_view_all_link()
        popular_apps_search_results = popular_apps_search_page.results
        Assert.true(len(popular_apps_search_results) == 25)
        popular_apps_search_page.scroll_to_last_result_item()
        Assert.true(popular_apps_search_page.is_more_button_visible)

        home_page.go_to_homepage()
        new_apps = home_page.click_new_category_tab()

        Assert.true(home_page.is_new_category_tab_selected)
        new_apps_search_page = home_page.click_new_popular_view_all_link()
        new_apps_search_results = new_apps_search_page.results
        Assert.true(len(new_apps_search_results) == 25)
        new_apps_search_page.scroll_to_last_result_item()
        Assert.true(new_apps_search_page.is_more_button_visible)
