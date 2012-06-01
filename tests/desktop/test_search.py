#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from unittestzero import Assert

from pages.desktop.consumer_pages.home import Home


class TestSearching:

    def test_that_searching_with_empty_field_using_the_arrow_button_returns_results(self, mozwebqa):
        """Litmus 58181"""
        home_page = Home(mozwebqa)

        home_page.go_to_homepage()
        home_page.login()

        Assert.true(home_page.is_the_current_page)
        search_page = home_page.header.search(click_arrow=True)

        Assert.true(search_page.is_the_current_page)
        Assert.greater(len(search_page.results), 0)

    def test_that_searching_with_empty_field_using_submit_returns_results(self, mozwebqa):
        """Litmus 58181"""
        home_page = Home(mozwebqa)

        home_page.go_to_homepage()
        home_page.login()

        Assert.true(home_page.is_the_current_page)
        search_page = home_page.header.search(click_arrow=False)

        Assert.true(search_page.is_the_current_page)
        Assert.greater(len(search_page.results), 0)

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

    def test_that_verifies_the_sort_region_from_searc_results(self, mozwebqa):
        """Litmus 58183"""

        search_term = "SeaVan"
        sort_filers = ["Newest", "Relevance", "Weekly Downloads", "Top Rated", "Price"]

        home_page = Home(mozwebqa)

        home_page.go_to_homepage()
        home_page.login()

        Assert.true(home_page.is_the_current_page)
        search_page = home_page.header.search(search_term)
        Assert.equal("Relevance", search_page.sorted_by)
        Assert.equal("Sort by:", search_page.sorter_header)

        # Test that the filters are applicable on the results
        for sort_filter in sort_filers:
            search_page.sort_by(sort_filter)
            Assert.equal(sort_filter, search_page.sorted_by)
            Assert.greater(len(search_page.results), 0)
