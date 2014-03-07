#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert
from selenium import webdriver

from persona_test_user import PersonaTestUser
from mocks.marketplace_api import MarketplaceAPI
from mocks.mock_review import MockReview
from pages.desktop.consumer_pages.home import Home
from requests.exceptions import HTTPError


class TestReviews:

    def _reviews_setup(self, mozwebqa):
        # init API client
        self.mk_api = MarketplaceAPI.get_client(mozwebqa.base_url,
                                                mozwebqa.credentials)

        # Submit a review using marketplace API
        mock_review = MockReview()
        home_page = Home(mozwebqa)
        self.app_name, self.review_id = self.mk_api.submit_app_review_for_either(
            home_page.app_under_test,
            mock_review.body,
            mock_review.rating)

    @pytest.mark.xfail(reason='Bug 980799 - [dev][stage] Adding review to an app does not appear, only after page reload')
    def test_that_checks_the_addition_of_a_review(self, mozwebqa):
        self._reviews_setup(mozwebqa)

        # delete the review before getting started
        self.mk_api.delete_app_review(self.review_id)

        # so that teardown does not try to delete the review
        del self.review_id

        # Step 1 - Login into Marketplace
        mock_review = MockReview()
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        home_page.login(user="default")
        Assert.true(home_page.is_the_current_page)

        # Step 2 - Search for the test app and go to its details page
        search_page = home_page.header.search(self.app_name)
        details_page = search_page.results[0].click_name()
        Assert.true(details_page.is_the_current_page)

        Assert.true(details_page.is_write_review_button_visible)
        Assert.equal(details_page.write_review_button, "Write a Review")

        # Step 3 - Write a review
        add_review_box = details_page.click_write_review()
        details_page = add_review_box.write_a_review(mock_review['rating'], mock_review['body'])

        # Step 4 - Check review
        details_page.wait_notification_box_visible()
        Assert.equal(details_page.notification_message, "Your review was posted")
        details_page.wait_notification_box_not_visible()

        Assert.equal(details_page.first_review_rating, mock_review['rating'])
        Assert.equal(details_page.first_review_body, mock_review['body'])

        # Clean up
        reviews_page = details_page.click_reviews_button()
        reviews = reviews_page.reviews[0]
        reviews.delete()

    @pytest.mark.xfail(reason='Bug 980799 - [dev][stage] Adding review to an app does not appear, only after page reload')
    def test_that_checks_the_editing_of_a_review(self, mozwebqa):

        self._reviews_setup(mozwebqa)

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        # Login into Marketplace
        home_page.login(user="default")
        Assert.true(home_page.is_the_current_page)

        # Search for the test app and go to its details page
        search_page = home_page.header.search(self.app_name)
        details_page = search_page.results[0].click_name()
        Assert.true(details_page.is_the_current_page)

        Assert.true(details_page.is_edit_review_button_visible)
        Assert.equal(details_page.edit_review_button, "Edit Your Review")

        # Write a review
        edit_review = details_page.click_edit_review()
        mock_review = MockReview()
        details_page = edit_review.write_a_review(mock_review['rating'], mock_review['body'])

        # Check notification
        details_page.wait_notification_box_visible()
        Assert.equal(details_page.notification_message, "Review updated successfully")
        details_page.wait_notification_box_not_visible()

        # Go to reviews page and verify
        reviews = details_page.click_reviews_button()
        Assert.equal(reviews.logged_in_users_review.text, mock_review['body'])
        Assert.equal(reviews.logged_in_users_review.rating, mock_review['rating'])

        # Clean up
        self.mk_api.delete_app_review(self.review_id)

    @pytest.mark.xfail(reason='Bug 980799 - [dev][stage] Adding review to an app does not appear, only after page reload')
    def test_that_checks_the_deletion_of_a_review(self, mozwebqa):
        """
        https://moztrap.mozilla.org/manage/case/648/
        """

        self._reviews_setup(mozwebqa)

        # Step 1 - Login into Marketplace
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        home_page.login(user="default")
        Assert.true(home_page.is_the_current_page)

        # Step 3 - Search for the test app and go to its details page
        search_page = home_page.header.search(self.app_name)
        details_page = search_page.results[0].click_name()
        Assert.true(details_page.is_the_current_page)

        # Step 4 - Go to reviews page
        reviews_page = details_page.click_reviews_button()

        # Step 5 - Delete review
        reviews = reviews_page.reviews[0]
        reviews.delete()

        reviews_page.wait_notification_box_visible()
        Assert.equal(reviews_page.notification_message, "Review deleted")
        Assert.false(reviews.is_review_visible)

    def teardown(self):
        # Clean up review for the tests that create a new review
        if hasattr(self, 'review_id'):
            try:
                self.mk_api.delete_app_review(self.review_id)
            except HTTPError:
                # don't do anything when this exception is raised as
                # test_that_checks_the_deletion_of_a_review probably passed
                pass
