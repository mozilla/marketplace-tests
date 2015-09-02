#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.mobile.home import Home
from mocks.mock_review import MockReview
from tests.base_test import BaseTest


class TestReviews(BaseTest):

    def test_that_after_writing_a_review_clicking_back_goes_to_app_page(self, mozwebqa, new_user):
        """Logged out, click "Write a Review" on an app page, sign in, submit a review,
        click Back, test that the current page is the app page.
        """
        mock_review = MockReview()

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        details_page = home_page.go_to_first_free_app_page()
        assert details_page.is_product_details_visible
        app_name = details_page.title

        # Write a review.
        review_box = details_page.click_write_review()
        details_page.login(new_user['email'], new_user['password'])

        review_box.write_a_review(mock_review['rating'], mock_review['body'])

        assert 'Your review was successfully posted. Thanks!' == details_page.notification_message
        details_page.wait_notification_box_not_visible()

        # Go to the reviews page
        reviews_page = details_page.click_view_reviews()
        reviews_page.header.click_back()
        assert details_page.is_product_details_visible
        assert app_name == details_page.title

    @pytest.mark.nondestructive
    def test_that_after_viewing_reviews_clicking_back_goes_to_app_page(self, mozwebqa):
        """ Navigate to the reviews listing for an app from the URL (not by clicking through to it),
        click back, test that the current page is the app page.
        """
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        details_page = home_page.go_to_first_free_app_page()
        app_name = details_page.title
        reviews_page = details_page.go_to_reviews_page()
        assert reviews_page.is_the_current_page

        reviews_page.header.click_back()
        assert details_page.is_product_details_visible
        assert app_name in details_page.title

    def test_that_checks_the_addition_of_a_review(self, mozwebqa, new_user):
        mock_review = MockReview()
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        home_page.nav_menu.click_sign_in()
        home_page.login(new_user['email'], new_user['password'])
        details_page = home_page.go_to_first_free_app_page()
        assert details_page.is_product_details_visible

        # Write a review
        review_box = details_page.click_write_review()
        review_box.write_a_review(mock_review['rating'], mock_review['body'])
        assert 'Your review was successfully posted. Thanks!' == details_page.notification_message
        details_page.wait_notification_box_not_visible()

        # Go to the reviews page
        reviews_page = details_page.click_view_reviews()

        # Check review
        review = reviews_page.reviews[0]
        assert mock_review['rating'] == review.rating
        assert review.author in new_user['email']
        assert mock_review['body'] in review.text
