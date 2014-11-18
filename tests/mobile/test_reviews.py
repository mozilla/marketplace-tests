#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from unittestzero import Assert
import pytest

from pages.mobile.home import Home
from mocks.marketplace_api import MarketplaceAPI
from mocks.mock_review import MockReview
from pages.mobile.reviews import Reviews
from pages.mobile.details import Details


class TestReviews():

    def _reviews_setup(self, mozwebqa):
        self.mk_api = MarketplaceAPI.get_client(mozwebqa.base_url, mozwebqa.credentials)

    def test_that_after_writing_a_review_clicking_back_goes_to_app_page(self, mozwebqa):
        """Logged out, click "Write a Review" on an app page, sign in, submit a review,
        click Back, test that the current page is the app page.
        """
        self._reviews_setup(mozwebqa)

        mock_review = MockReview()

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        app_name = home_page.app_under_test

        # Search for an app and go to it's details page.
        search_page = home_page.search_for(app_name)
        details_page = search_page.results[0].click_app()

        Assert.true(details_page.is_product_details_visible)

        # Write a review.
        review_box = details_page.click_write_review()
        details_page.login_with_user_from_other_pages(user="default")
        self.review_id = review_box.write_a_review(mock_review['rating'], mock_review['body']).review_id

        Assert.equal(details_page.notification_message, "Your review was posted")
        details_page.wait_notification_box_not_visible()

        # Go to the reviews page and delete the review
        reviews_page = details_page.click_view_reviews()
        reviews = reviews_page.reviews[0]
        reviews.delete()
        reviews_page.wait_notification_box_visible()

        Assert.equal(details_page.notification_message, "Review deleted")

        # if clean up was successful, don't cleanup in teardown
        del self.review_id

        # After clicking back, current page is the app's details page.
        reviews_page.header.click_back()

        Assert.true(details_page.is_product_details_visible)
        Assert.equal(app_name, details_page.title)

    @pytest.mark.nondestructive
    def test_that_after_viewing_reviews_clicking_back_goes_to_app_page(self, mozwebqa):
        """ Navigate to the reviews listing for an app from the URL (not by clicking through to it),
        click back, test that the current page is the app page.
        """

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        reviews_page = Reviews(mozwebqa)
        app_name = reviews_page.app_under_test

        reviews_page.go_to_reviews_page(app_name)

        Assert.true(reviews_page.is_reviews_list_visible)

        details_page = Details(mozwebqa)
        reviews_page.header.click_back()

        Assert.true(details_page.is_product_details_visible)
        Assert.equal(app_name, details_page.title)

    @pytest.mark.xfail(reason='Until issue https://github.com/mozilla/marketplace-tests/issues/568 is fixed')
    def test_that_checks_the_addition_of_a_review(self, mozwebqa):
        self._reviews_setup(mozwebqa)

        mock_review = MockReview()

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        app_name = home_page.app_under_test

        # Login
        settings_page = home_page.header.click_settings()
        settings_page.login(user='default')
        settings_page.wait_for_user_email_visible()

        # Search for an app and go to it's details page.
        search_page = home_page.search_for(app_name)
        details_page = search_page.results[0].click_app()
        Assert.true(details_page.is_product_details_visible)

        # Write a review
        details_page.refresh_page()
        review_box = details_page.click_write_review()
        self.review_id = review_box.write_a_review(mock_review['rating'], mock_review['body']).review_id

        Assert.equal(details_page.notification_message, "Your review was posted")
        details_page.wait_notification_box_not_visible()

        # Go to the reviews page
        reviews_page = details_page.click_view_reviews()

        # Check review
        review = reviews_page.reviews[0]
        Assert.equal(review.rating, mock_review['rating'])
        Assert.contains(review.author, mozwebqa.credentials['default']['email'])
        Assert.contains(review.text, mock_review['body'])

        # clean up
        review.delete()
        reviews_page.wait_notification_box_visible()

        # if clean up was successful, don't cleanup in teardown
        del self.review_id

    def teardown(self):
        if hasattr(self, 'review_id'):
            # if the tests fail to clean-up, use the api and clean-up
            self.mk_api.delete_app_review(self.review_id)
