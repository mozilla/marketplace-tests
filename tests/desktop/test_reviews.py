#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest
from unittestzero import Assert

from pages.desktop.consumer_pages.home import Home


class TestReviews:

    def test_that_checks_the_addition_of_a_review(self, mozwebqa):
        home_page = Home(mozwebqa)

        home_page.go_to_homepage()
        home_page.login()

        Assert.true(home_page.is_the_current_page)

        # search for a mock app and click on the first result
        search_page = home_page.header.search("mock application")
        details_page = search_page.results[0].click_name()

        Assert.true(details_page.is_the_current_page)

        Assert.true(details_page.is_submit_review_link_visible)
        Assert.equal(details_page.submit_review_link, "Submit a Review")
