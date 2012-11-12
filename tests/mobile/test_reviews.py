#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from unittestzero import Assert

from pages.mobile.reviews import Reviews
from pages.mobile.details import Details


class TestReviews():

    app_name = "Hypno"

    def test_that_after_viewing_reviews_clicking_back_goes_to_app_page(self, mozwebqa):
        """ Navigate to the reviews listing for an app from the URL (not by clicking through to it),
        click back, test that the current page is the app page.
        """
        reviews_page = Reviews(mozwebqa)
        reviews_page.go_to_reviews_page(self.app_name)
        Assert.true(reviews_page.is_the_current_page)

        reviews_page.header.click_back()
        details_page = Details(mozwebqa)
        Assert.true(details_page.is_the_current_page)
        Assert.equal(self.app_name, details_page.title)
