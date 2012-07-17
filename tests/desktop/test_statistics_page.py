#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from selenium.common.exceptions import InvalidElementStateException
from unittestzero import Assert
from pages.desktop.consumer_pages.home import Home


class TestStatistics:
        @pytest.mark.nondestructive
        def test_statistics_graph_is_visible(self, mozwebqa):
            search_term = "Evernote"

            home_page = Home(mozwebqa)
            home_page.go_to_homepage()
            search_page = home_page.header.search(search_term)
            evernote_details = search_page.results[0].click_name()
            statistics_page = evernote_details.click_statistics()
            Assert.true(statistics_page.is_chart_visible)

        @pytest.mark.nondestructive
        def test_report_date_validity(self, mozwebqa):
            """Checks the first Date of the report
            is today's date or yesterday's date"""
            search_term = "Evernote"

            home_page = Home(mozwebqa)
            home_page.go_to_homepage()
            search_page = home_page.header.search(search_term)
            evernote_details = search_page.results[0].click_name()
            statistics_page = evernote_details.click_statistics()

            Assert.true(statistics_page.verify_report_start)

        @pytest.mark.nondestructive
        def test_next_report_navigation(self, mozwebqa):
            search_term = "Evernote"
            i = 0

            home_page = Home(mozwebqa)
            home_page.go_to_homepage()
            search_page = home_page.header.search(search_term)
            evernote_details = search_page.results[0].click_name()
            statistics_page = evernote_details.click_statistics()
            Assert.true(statistics_page.is_prev_disabled)

            for i in range(0, 10):

                next_report = statistics_page.click_next_button()
                Assert.true(statistics_page.is_prev_visible)
                Assert.false(statistics_page.is_prev_disabled)

            for i in range(0, 10):

                next_report = statistics_page.click_prev_button()
                Assert.true(statistics_page.is_prev_visible)

            Assert.true(statistics_page.is_prev_disabled)
