#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from pages.mobile.home import Home
from tests.mobile.base_test import BaseTest

class TestHomepage(BaseTest):

    @pytest.mark.nondestructive
    def test_that_verifies_featured_application_section(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        #Assert.true(home_page.is_the_current_page)

        # Check if featured section is visible and contains applications
        Assert.true(home_page.is_featured_section_visible)
        Assert.equal(home_page.featured_section_elements_count, 6)

    @pytest.mark.nondestructive
    def test_that_verifies_categories_section(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        #Assert.true(home_page.is_the_current_page)

        Assert.true(home_page.is_category_section_visible)
        Assert.equal(len(home_page.categories.items), 6)
