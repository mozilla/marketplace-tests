#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest

from unittestzero import Assert

from pages.desktop.consumer_pages.home import Home


class TestConsumerPage:

    @pytest.mark.action_chains
    @pytest.mark.nondestructive
    def test_that_header_has_expected_items(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.true(home_page.header.is_logo_visible)
        Assert.true(home_page.header.is_search_visible)
        Assert.equal(home_page.header.search_field_placeholder, "Search")
        Assert.true(home_page.header.is_sign_in_visible)

    @pytest.mark.nondestructive
    def test_that_verifies_categories_menu(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.equal(home_page.categories.title, 'Categories'.upper())

        # Hover over "Categories" menu
        home_page.hover_over_categories_menu()
        Assert.greater(len(home_page.categories.items), 0)

    @pytest.mark.nondestructive
    def test_opening_every_category_page_from_categories_menu(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        for i in range(home_page.category_count):
            home_page.hover_over_categories_menu()
            category_name = home_page.categories.items[i].name
            category_page = home_page.categories.items[i].click_category()
            Assert.equal(category_name, category_page.category_title)
            Assert.true(category_page.is_the_current_page)

    @pytest.mark.nondestructive
    def test_that_verifies_nav_menu_tabs(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.true('Home'.upper() in home_page.selected_tab_text)

        home_page.click_new_tab()
        Assert.true('New'.upper() in home_page.selected_tab_text)
        Assert.true(home_page.apps_are_visible)
        Assert.true(home_page.elements_count > 0)

        home_page.click_new_tab()
        Assert.true('Popular'.upper() in home_page.selected_tab_text)
        Assert.true(home_page.apps_are_visible)
        Assert.true(home_page.elements_count > 0)
