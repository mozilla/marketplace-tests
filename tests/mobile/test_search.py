#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from tests.mobile.base_test import BaseTest
from pages.mobile.home import Home


class TestSearch(BaseTest):

    search_term = "Hypno"

    @pytest.mark.nondestructive
    def test_that_searching_with_empty_field_returns_results(self, mozwebqa):
        home_page = Home(mozwebqa)

        home_page.go_to_homepage()

        #Assert.true(home_page.is_the_current_page)
        search_page = self.search(home_page, "")

        #Assert.true(search_page.is_the_current_page)
        Assert.greater(len(search_page.results), 0)
