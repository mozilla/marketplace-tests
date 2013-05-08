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
