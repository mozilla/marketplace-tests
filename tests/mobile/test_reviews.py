#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from unittestzero import Assert

from pages.mobile.home import Home
from mocks.mock_review import MockReview
from pages.mobile.reviews import Reviews
from pages.mobile.details import Details
from tests.base_test import BaseTest


class TestReviews(BaseTest):

    def _take_first_app_name(self, mozwebqa):
        home_page = Home(mozwebqa)
        app_name = home_page.first_app_name
        return app_name

    @pytest.mark.xfail(reason='Bug 1130986 - [dev][stage] Review box is not displayed after user logs in from an app details page')
    def test_that_after_writing_a_review_clicking_back_goes_to_app_page(self, mozwebqa):
        """Logged out, click "Write a Review" on an app page, sign in, submit a review,
        click Back, test that the current page is the app page.
        """
        mock_review = MockReview()

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        # Search for an app and go to it's details page.
        search_term = self._take_first_app_name(mozwebqa)
        details_page = home_page.search_and_click_on_app(search_term)
        Assert.true(details_page.is_product_details_visible)

        # Write a review.
        review_box = details_page.click_write_review()
        acct = self.create_new_user(mozwebqa)
        details_page.login(acct)

        self.review_id = review_box.write_a_review(mock_review['rating'], mock_review['body']).review_id

        Assert.equal(details_page.notification_message, "Your review was successfully posted. Thanks!")
        details_page.wait_notification_box_not_visible()

        # Go to the reviews page
        reviews_page = details_page.click_view_reviews()
        reviews_page.header.click_back()

        Assert.true(details_page.is_product_details_visible)
        Assert.equal(search_term, details_page.title)

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
        Assert.contains(app_name, details_page.title)

    def test_that_checks_the_addition_of_a_review(self, mozwebqa):

        mock_review = MockReview()

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        app_name = self._take_first_app_name(mozwebqa)

        # Login
        settings_page = home_page.header.click_settings()
        settings_page.click_sign_in()
        acct = self.create_new_user(mozwebqa)
        settings_page.login(acct)
        settings_page.wait_for_user_email_visible()

        # Search for an app and go to it's details page.
        search_page = home_page.search_for(app_name)
        details_page = search_page.results[0].click_app()
        Assert.true(details_page.is_product_details_visible)

        # Write a review
        details_page.refresh_page()
        review_box = details_page.click_write_review()
        self.review_id = review_box.write_a_review(mock_review['rating'], mock_review['body']).review_id

        Assert.equal(details_page.notification_message, "Your review was successfully posted. Thanks!")
        details_page.wait_notification_box_not_visible()

        # Go to the reviews page
        reviews_page = details_page.click_view_reviews()

        # Check review
        review = reviews_page.reviews[0]
        Assert.equal(review.rating, mock_review['rating'])
        Assert.contains(review.author, acct.email)
        Assert.contains(review.text, mock_review['body'])
