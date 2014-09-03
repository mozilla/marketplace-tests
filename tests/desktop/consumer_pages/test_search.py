#!/usr/bin/env python
# -*- coding: utf-8-*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from pages.desktop.consumer_pages.home import Home


class TestSearching:

    sort_search_term = 'test'

    def _take_first_new_app_name(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.click_new_tab()
        app_name = home_page.first_new_app_name
        return app_name

    @pytest.mark.nondestructive
    def test_that_searching_with_empty_field_using_submit_returns_results(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.true(home_page.is_the_current_page)
        search_page = home_page.header.search("")

        Assert.true(search_page.is_the_current_page)
        Assert.greater(len(search_page.results), 0)

    @pytest.mark.sanity
    @pytest.mark.nondestructive
    def test_that_the_search_tag_is_present_in_the_search_results(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        search_term = self._take_first_new_app_name(mozwebqa)
        search_page = home_page.header.search(search_term)

        # Check title for the search
        Assert.contains('Result', search_page.search_results_section_title)

        # Check that the results contains the search term
        # Bug 1058467 - [prod] Search results are not very exact
        # We change the weights of search results based on popularity. That is why you see other apps in there.
        for i in range(len(search_page.results)):
            if search_term == search_page.results[i].name:
                Assert.equal(search_term, search_page.results[i].name)

    @pytest.mark.skipif('True', reason='Sort not available yet.')
    @pytest.mark.nondestructive
    @pytest.mark.parametrize(('sort_type'), ["Relevancy", "Rating"])
    def test_that_verifies_the_sort_region_from_search_results(self, mozwebqa, sort_type):

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

    @pytest.mark.skipif('True', reason='Search suggestions not available yet.')
    @pytest.mark.nondestructive
    def test_that_verifies_the_search_suggestions_list_under_the_search_field(self, mozwebqa):

        home_page = self._take_random_new_app_name(mozwebqa)

        Assert.true(home_page.is_the_current_page)

        search_term = self._take_first_new_app_name(mozwebqa)

        home_page.header.type_search_term_in_search_field(search_term)
        Assert.true(home_page.header.is_search_suggestion_list_visible)
        Assert.greater_equal(len(home_page.header.search_suggestions), 0)

        for suggestion in home_page.header.search_suggestions:
            Assert.contains(search_term, suggestion.app_name)

    @pytest.mark.nondestructive
    def test_that_checks_search_with_foreign_characters(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        foreign_search_term = 'dödá pápègoján'.decode('utf-8')
        search_page = home_page.header.search(foreign_search_term)

        Assert.true(search_page.is_the_current_page)
        Assert.contains(foreign_search_term, search_page.page_title)

    @pytest.mark.sanity
    @pytest.mark.nondestructive
    def test_search_results_page_items(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        search_term = self._take_first_new_app_name(mozwebqa)
        search_page = home_page.header.search(search_term)

        search_page.click_on_expand_button()

        for i in range(len(search_page.results)):
            Assert.true(search_page.results[i].install_button_visible)
            Assert.true(search_page.results[i].icon_visible)
            Assert.true(search_page.results[i].ratings_visible)
            Assert.true(search_page.results[i].reviews_number_visible)
            Assert.true(search_page.results[i].screenshots_visible)
