#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from pages.mobile.home import Home


class TestDetails():

    @pytest.mark.nondestructive
    def test_details_page_for_an_app(self, mozwebqa):
        """https://moztrap.mozilla.org/runtests/run/243/env/112/ - Verify details page for an app"""
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        #first app name
        first_featured_app_name = home_page.featured_apps[1].name

        #click first app and load its Details Page
        details_page = home_page.featured_apps[1].click()
        details_page.click_more_button()

        #The verifications required by the testcase
        Assert.true(details_page.header.is_back_button_visible)
        Assert.true(first_featured_app_name in details_page.title)
        Assert.true(details_page.is_author_visible)
        Assert.true(details_page.is_app_icon_present)
        Assert.true(details_page.is_rating_visible)
        Assert.true(details_page.is_product_details_visible)
        Assert.true(details_page.is_description_visible)

    @pytest.mark.nondestructive
    def test_reviews_section(self, mozwebqa):
        """https://moztrap.mozilla.org/runtests/run/243/env/112/ - Verify details page for an app - Reviews section"""
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        #click first app and load its Details Page
        details_page = home_page.featured_apps[0].click()

        #This takes the number of reviews on the details page and based on that number it treats 3 different scenarios:
        #when the app has reviews, when it has 1 review and when the app isn't rated.
        if details_page.is_app_rated:
            if details_page.reviews_count >= 2:
                if len(details_page.reviews) == 2:
                    for review in details_page.reviews:
                        Assert.true(review.is_visible)
            elif details_page.reviews_count == 1:
                Assert.true(details_page.reviews.is_visible)
        else:
            Assert.equal(details_page.app_not_rated_text, 'This app is not yet rated.')

        Assert.true(details_page.is_write_a_review_button_visible)

        for support_button in details_page.support_buttons:
            Assert.true(support_button.is_visible)
