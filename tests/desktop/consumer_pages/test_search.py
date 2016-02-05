#!/usr/bin/env python
# -*- coding: utf-8-*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from tests.base_test import BaseTest
from pages.desktop.consumer_pages.home import Home


class TestSearching(BaseTest):

    sort_search_term = 'test'

    @pytest.mark.nondestructive
    def test_that_searching_with_empty_field_using_submit_returns_results(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        home_page.go_to_homepage()
        assert home_page.is_the_current_page

        search_page = home_page.header.search("")
        assert search_page.is_the_current_page
        assert len(search_page.results) > 0

    @pytest.mark.sanity
    @pytest.mark.nondestructive
    def test_that_the_search_tag_is_present_in_the_search_results(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        home_page.go_to_homepage()
        search_term = self._take_first_free_app_name(base_url, selenium)
        search_page = home_page.header.search(search_term)
        assert 'result' in search_page.search_results_section_title

        # Check that the results contains the search term
        for i in range(len(search_page.results)):
            if search_term == search_page.results[i].name:
                # FIXME: This assertion will never fail
                assert search_term == search_page.results[i].name

    @pytest.mark.nondestructive
    def test_that_checks_search_with_foreign_characters(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        home_page.go_to_homepage()
        foreign_search_term = 'dödá pápègoján'.decode('utf-8')
        search_page = home_page.header.search(foreign_search_term)
        assert search_page.is_the_current_page
        assert foreign_search_term in search_page.page_title

    @pytest.mark.sanity
    @pytest.mark.nondestructive
    def test_results_page_items(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        home_page.go_to_homepage()
        search_term = self._take_first_free_app_name(base_url, selenium)
        search_page = home_page.header.search(search_term)
        search_page.click_expand_button()
        results = search_page.results

        # check the first 5 results
        for i in range(min(len(results), 5)):
            assert results[i].is_install_button_visible
            assert results[i].is_icon_visible
            assert results[i].is_rating_visible
            assert results[i].are_screenshots_visible
