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

        Assert.false(home_page.header.menu.is_menu_visible, "Menu open at page open")

        # open menu and verify visibility
        home_page.header.menu.open_menu()
        Assert.true(home_page.header.menu.is_menu_visible, "Menu is not open")

        # verify menu item names
        expected_menu = ["Home", "Popular", "Top Free", "Top Paid", "Categories"]
        Assert.equal(expected_menu, [ item.name for item in home_page.header.menu.items ],
                     "Unexpected menu item")

        # close menu and verify
        home_page.header.menu.close_menu()
        Assert.false(home_page.header.menu.is_menu_visible, "Menu did not close")

    @pytest.mark.nondestructive
    def test_that_verifies_the_most_popular_section(self, mozwebqa):
        '''https://www.pivotaltracker.com/projects/477093 ID:31913803'''

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.true(home_page.is_the_current_page)

        # Check if the most popular section title is visible
        Assert.true(home_page.is_most_popular_section_title_visible)

        # Check if the most popular section is visible and contains applications
        Assert.true(home_page.is_most_popular_section_visible)
        for element in home_page.popular_section_elements_list:
            if element in home_page.popular_section_elements_list[:-1]:
                Assert.true(element.is_displayed())
            else:
                Assert.false(home_page.popular_section_elements_list[-1].is_displayed())

    @pytest.mark.nondestructive
    def test_that_verifies_featured_application_section(self, mozwebqa):
        '''https://www.pivotaltracker.com/projects/477093 ID:31913881'''

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.true(home_page.is_the_current_page)

        # Check if featured application section title is visible
        Assert.true(home_page.is_featured_section_title_visible)

        # Check if featured section is visible and contains applications
        Assert.true(home_page.is_featured_section_visible)
        Assert.equal(home_page.featured_section_elements_count, 3)

    @pytest.mark.nondestructive
    def test_that_verifies_categories_section(self, mozwebqa):
        """https://www.pivotaltracker.com/story/show/31913855"""

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.equal(len(home_page.category_items), 15)
