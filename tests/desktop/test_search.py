#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest
from unittestzero import Assert

from pages.desktop.consumer_pages.home import Home
from pages.desktop.regions.filter import FilterTags


class TestSearching:

    @pytest.mark.nondestructive
    def test_that_searching_with_empty_field_using_the_arrow_button_returns_results(self, mozwebqa):
        """Litmus 58181"""
        home_page = Home(mozwebqa)

        home_page.go_to_homepage()
        home_page.login()

        Assert.true(home_page.is_the_current_page)
        search_page = home_page.header.search("", click_arrow=True)

        Assert.true(search_page.is_the_current_page)
        Assert.greater(len(search_page.results), 0)

    @pytest.mark.nondestructive
    def test_that_searching_with_empty_field_using_submit_returns_results(self, mozwebqa):
        """Litmus 58181"""
        home_page = Home(mozwebqa)

        home_page.go_to_homepage()
        home_page.login()

        Assert.true(home_page.is_the_current_page)
        search_page = home_page.header.search("", click_arrow=False)

        Assert.true(search_page.is_the_current_page)
        Assert.greater(len(search_page.results), 0)

    @pytest.mark.nondestructive
    def test_that_the_search_tag_is_present_in_the_search_results(self, mozwebqa):
        """Litmus 53263"""

        search_term = "SeaVan"
        home_page = Home(mozwebqa)

        home_page.go_to_homepage()
        home_page.login()

        Assert.true(home_page.is_the_current_page)
        search_page = home_page.header.search(search_term)

        # Check page title
        Assert.equal("%s | Search | Mozilla Marketplace" % search_term, search_page.page_title)

        # Check the breadcrumbs
        Assert.equal("Home", search_page.breadcrumbs[0].text)
        Assert.equal("Search", search_page.breadcrumbs[1].text)
        Assert.equal("SeaVan", search_page.breadcrumbs[2].text)

        # Check title for the search
        Assert.equal('Search Results for "%s"' % search_term, search_page.title)

        # Check that the first result contains the search term
        Assert.contains(search_term, search_page.results[0].name)

    @pytest.mark.parametrize(('sort_type'), ["Newest", "Relevance", "Weekly Downloads", "Top Rated", "Price"])
    @pytest.mark.nondestructive
    def test_that_verifies_the_sort_region_from_search_results(self, mozwebqa, sort_type):
        """Litmus 58183"""

        search_term = "SeaVan"

        home_page = Home(mozwebqa)

        home_page.go_to_homepage()
        home_page.login()

        Assert.true(home_page.is_the_current_page)
        search_page = home_page.header.search(search_term)
        Assert.equal("Relevance", search_page.sorted_by)
        Assert.equal("Sort by:", search_page.sorter_header)

        # Test that the filters are applicable on the results

        search_page.sort_by(sort_type)
        Assert.equal(sort_type, search_page.sorted_by)
        Assert.greater(len(search_page.results), 0)

    @pytest.mark.nondestructive
    @pytest.mark.parametrize(('search_filter'), FilterTags.category)
    def test_filtering_apps_by_category(self, mozwebqa, search_filter):
        home_page = Home(mozwebqa)

        home_page.go_to_homepage()
        home_page.login()

        Assert.true(home_page.is_the_current_page)
        search_page = home_page.header.search("")

        result_count_before_filter = search_page.results_count

        Assert.greater(result_count_before_filter, 0, "No results on the page")

        search_page.filter_by(search_filter).click()
        result_count_after_filter = search_page.results_count

        Assert.greater(result_count_before_filter, result_count_after_filter)
        Assert.contains(search_filter, search_page.applied_filters)

        [Assert.contains(search_filter, item.categories) for item in search_page.results]
