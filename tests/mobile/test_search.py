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

        search_page = self.search(home_page, "")

        Assert.greater(len(search_page.results), 0)

    @pytest.mark.nondestructive
    def test_that_searching_returns_results(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        search_page = self.search(home_page, self.search_term)

        Assert.greater(len(search_page.results), 0)

        Assert.contains(self.search_term, search_page.results[0].name)

    @pytest.mark.nondestructive
    @pytest.mark.xfail(reason="Bug 764303 - Search suggestions not working")
    def test_that_verifies_the_search_suggestions_list_under_the_search_field(self, mozwebqa):

        home_page = Home(mozwebqa)

        home_page.go_to_homepage()

        home_page.header.click_search()
        Assert.true(home_page.header.is_search_visible)

        for letter in self.search_term[:2]:
            home_page.header.type_in_search_field(letter)
            Assert.false(home_page.header.is_search_suggestions_visible)

        home_page.header.type_in_search_field(self.search_term[2])
        home_page.header.wait_for_suggestions()
        Assert.true(home_page.header.is_search_suggestions_visible)

        Assert.equal(home_page.header.search_suggestions_title, 'Search apps for "%s"' % self.search_term[:3])
        Assert.greater_equal(len(home_page.header.search_suggestions), 0)

        for suggestion in home_page.header.search_suggestions:
            Assert.contains(self.search_term[:3], suggestion.name)
            Assert.true(suggestion.is_icon_visible)
