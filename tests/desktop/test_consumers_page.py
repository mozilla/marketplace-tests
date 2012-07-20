#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest

from unittestzero import Assert

from pages.desktop.consumer_pages.home import Home


class TestConsumerPage:

    @pytest.mark.nondestructive
    def test_most_important_section(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.true(home_page.is_the_current_page)

        # Check if the most popular section title is visible
        Assert.true(home_page.is_most_popular_section_title_visible)

        # Check if the most popular section contains applications
        Assert.true(home_page.is_most_popular_section_visible)
