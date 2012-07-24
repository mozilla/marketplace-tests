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
        Assert.true(home_page.does_most_popular_section_contain_applications == 9)


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
        Assert.true(home_page.does_featured_section_contain_applications == 3)
