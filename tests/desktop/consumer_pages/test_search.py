#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest
from unittestzero import Assert

from pages.desktop.consumer_pages.home import Home


class TestSearching:

    search_term = 'Lanyrd'
    sort_search_term = 'test'

    @pytest.mark.nondestructive
    def test_that_searching_with_empty_field_using_submit_returns_results(self, mozwebqa):
        """Litmus 58181"""
        home_page = Home(mozwebqa)

        home_page.go_to_homepage()

        Assert.true(home_page.is_the_current_page)
        search_page = home_page.header.search("")

        Assert.true(search_page.is_the_current_page)
        Assert.greater(len(search_page.results), 0)

    @pytest.mark.nondestructive
    def test_that_the_search_tag_is_present_in_the_search_results(self, mozwebqa):
        """Litmus 53263"""

        home_page = Home(mozwebqa)

        home_page.go_to_homepage()

        Assert.true(home_page.is_the_current_page)
        search_page = home_page.header.search(self.search_term)

        # Check title for the search
        Assert.contains('Result', search_page.search_results_section_title)

        # Check that the first result contains the search term
        Assert.contains(self.search_term, search_page.results[0].name)

    @pytest.mark.nondestructive
    @pytest.mark.parametrize(('sort_type'), ["Relevancy", "Rating"])
    def test_that_verifies_the_sort_region_from_search_results(self, mozwebqa, sort_type):
        """Litmus 58183"""
        if mozwebqa.base_url == 'https://marketplace-dev.allizom.org' or mozwebqa.base_url == 'https://marketplace.allizom.org' or mozwebqa.base_url == 'https://marketplace.firefox.com':
            pytest.skip('Sort not available yet.')
        home_page = Home(mozwebqa)

        home_page.go_to_homepage()

        Assert.true(home_page.is_the_current_page)
        search_page = home_page.header.search(self.sort_search_term)
        Assert.equal("Relevancy", search_page.sorted_by)
        Assert.true(search_page.is_sorter_header_visible)

        # Test that the filters are applicable on the results
        search_page.sort_by(sort_type)
        Assert.equal(sort_type, search_page.sorted_by)
        Assert.greater(len(search_page.results), 0)

    @pytest.mark.nondestructive
    def test_that_verifies_the_search_suggestions_list_under_the_search_field(self, mozwebqa):
        """
        Test for Litmus 66531
        https://litmus.mozilla.org/show_test.cgi?id=66531
        """
        if mozwebqa.base_url == 'https://marketplace-dev.allizom.org' or mozwebqa.base_url == 'https://marketplace.allizom.org' or mozwebqa.base_url == 'https://marketplace.firefox.com':
            pytest.skip('Search suggestions not available yet.')
        home_page = Home(mozwebqa)

        home_page.go_to_homepage()

        Assert.true(home_page.is_the_current_page)

        home_page.header.type_search_term_in_search_field(self.search_term)
        Assert.true(home_page.header.is_search_suggestion_list_visible)
        Assert.greater_equal(len(home_page.header.search_suggestions), 0)

        for suggestion in home_page.header.search_suggestions:
            Assert.contains(self.search_term, suggestion.app_name)

    @pytest.mark.nondestructive
    def test_that_checks_search_with_foreign_characters(self, mozwebqa):
        """Test for https://www.pivotaltracker.com/story/show/33702407"""

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        foreign_search_term = 'döda papegojan'.decode('utf-8')
        search_page = home_page.header.search(foreign_search_term)

        Assert.true(search_page.is_the_current_page)
        # TODO: enable title check when it's available
        # Assert.contains(foreign_search_term, search_page.search_results_section_title)
