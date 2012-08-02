#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest

from unittestzero import Assert

from pages.desktop.consumer_pages.home import Home


class TestConsumerPage:

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
    def test_that_checks_expanding_of_app_description(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        
        search_page = home_page.header.search('checkers')
        details_page = search_page.results[0].click_name()
        details_page.expand_app_description()

        Assert.true(details_page.is_app_description_expanded)
        Assert.greater(len(details_page.app_expanded_description_text), 0)