#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from unittestzero import Assert

from pages.mobile.home import Home
from mocks.mock_review import MockReview
from pages.mobile.add_review import AddReview
from pages.mobile.reviews import Reviews
from pages.mobile.details import Details


class TestReviews():

    app_name = "Hypno"

    def test_that_after_writing_a_review_clicking_back_goes_to_app_page(self, mozwebqa):
        """Logged out, click "Write a Review" on an app page, sign in, submit a review,
        click Back, test that the current page is the app page.
        """
        mock_review = MockReview()

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        # Search for an app and go to it's details page.
        search_page = home_page.search_for(self.app_name)

        details_page = search_page.results[0].click_app()

        Assert.true(details_page.is_product_details_visible)

        # Write a review.
        details_page.click_write_review()
        details_page.login_with_user_from_other_pages(user="default")
        add_review_page = AddReview(mozwebqa)
        review_page = add_review_page.write_a_review(mock_review['rating'], mock_review['body'])

        review_page.wait_for_ajax_on_page_finish()
        review_page.wait_for_reviews_visible()
        Assert.true(review_page.is_successful_message, "Review not added: %s" % review_page.notification_message)

        # After clicking back, current page is the app's details page.
        review_page.header.click_back()

        Assert.true(details_page.is_product_details_visible)
        Assert.equal(self.app_name, details_page.title)

    def test_that_after_viewing_reviews_clicking_back_goes_to_app_page(self, mozwebqa):
        """ Navigate to the reviews listing for an app from the URL (not by clicking through to it),
        click back, test that the current page is the app page.
        """
        reviews_page = Reviews(mozwebqa)
        reviews_page.go_to_reviews_page(self.app_name)

        Assert.true(reviews_page.is_reviews_list_visible)

        reviews_page.header.click_back()
        details_page = Details(mozwebqa)

        Assert.true(details_page.is_product_details_visible)
        Assert.equal(self.app_name, details_page.title)
