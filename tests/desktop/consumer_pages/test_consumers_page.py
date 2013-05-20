#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest

from unittestzero import Assert

from pages.desktop.consumer_pages.home import Home


class TestConsumerPage:

    @pytest.mark.nondestructive
    def test_that_header_menu_has_expected_items(self, mozwebqa):
        """
        Verify the menu opens & closes.  Verify menu item names
        """

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.true(home_page.header.is_logo_visible)
        Assert.true(home_page.header.is_search_visible)
        Assert.true(home_page.header.is_sign_in_visible)
        Assert.equal(home_page.header.search_field_placeholder, "Search")

    @pytest.mark.nondestructive
    def test_that_verifies_featured_application_section(self, mozwebqa):
        '''https://www.pivotaltracker.com/projects/477093 ID:31913881'''

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.true(home_page.is_the_current_page)

        # Check if featured section is visible and contains applications
        Assert.true(home_page.is_featured_section_visible)
        Assert.true(home_page.featured_section_elements_count > 0)

    @pytest.mark.nondestructive
    def test_that_verifies_categories_section(self, mozwebqa):
        """https://www.pivotaltracker.com/story/show/31913855"""

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.equal(home_page.categories.title, 'All Categories')

        # Open "All Categories" section
        home_page.expand_all_categories_section()
        Assert.greater(len(home_page.categories.items), 0)

    @pytest.mark.smoke
    @pytest.mark.nondestructive
    def test_that_clicking_on_featured_app_loads_details_page(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        details_page = home_page.click_on_first_app()
        Assert.true(details_page.is_the_current_page)

    @pytest.mark.nondestructive
    def test_opening_every_category_page_from_categories_section(self, mozwebqa):
        """In addition to Pivotal #31913855"""

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        for i in range(home_page.category_count):
            home_page.expand_all_categories_section()
            category_name = home_page.categories.items[i].name
            category_page = home_page.categories.items[i].click_category()
            Assert.true(category_name in category_page.title)
            Assert.true(category_page.is_the_current_page)
            home_page.go_to_homepage()
