# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from pages.mobile.home import Home


class TestSearch():

    @pytest.mark.nondestructive
    def test_that_searching_with_empty_field_returns_results(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        search_page = home_page.header.search('')

        Assert.greater(len(search_page.results()), 0)

    @pytest.mark.nondestructive
    def test_that_searching_returns_results(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        details_page = home_page.go_to_first_free_app_page()
        search_term = details_page.title
        details_page.header.click_back()
        search_page = home_page.header.search(search_term)

        results = search_page.results()
        Assert.greater(len(results), 0)

        # Check that the results contains the search term
        for i in range(len(results)):
            if search_term == results[i].name:
                return

        Assert.fail('The search results did not include the app: %s' % search_term)

    @pytest.mark.nondestructive
    def test_searching_with_no_matching_results(self, mozwebqa):
        search_term_with_no_result = 'abcdefghij'

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        search_page = home_page.header.search(search_term_with_no_result)

        Assert.equal('No results found', search_page.no_results_text)
