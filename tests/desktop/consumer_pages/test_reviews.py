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


class TestReviews:

    test_app = 'Twitter'

    @pytest.mark.skipif("webdriver.__version__ >= '2.32.0'", reason='Issue 5735: Firefox-Driver 2.33.0 falsely reports elements not to be visible')
    def test_that_checks_the_addition_of_a_review(self, mozwebqa):

        user = PersonaTestUser().create_user()

        # Step 1 - Login into Marketplace
        mock_review = MockReview()
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        home_page.login(user)
        Assert.true(home_page.is_the_current_page)

        # Step 2 - Search for the test app and go to its details page
        search_page = home_page.header.search(self.test_app)
        details_page = search_page.results[0].click_name()
        Assert.true(details_page.is_the_current_page)

        Assert.true(details_page.is_write_review_button_visible)
        Assert.equal(details_page.write_review_button, "Write a Review")

        # Step 3 - Write a review
        add_review_box = details_page.click_write_review()
        details_page = add_review_box.write_a_review(mock_review['rating'], mock_review['body'])

        # Step 4 - Check review
        Assert.true(details_page.notification_visible, "Review not added: %s" % details_page.success_message)
        Assert.equal(details_page.notification_message, "Your review was posted")
        Assert.equal(details_page.first_review_rating, mock_review['rating'])
        Assert.equal(details_page.first_review_body, mock_review['body'])

    @pytest.mark.xfail(reason="Need different apps for different tests for reviews. Issue https://github.com/mozilla/marketplace-tests/issues/320.")
    def test_that_checks_the_editing_of_a_review(self, mozwebqa):

        mk_api = MarketplaceAPI(credentials=mozwebqa.credentials['api'])  # init API client

        # Get test app's details
        app = mk_api.get_app(self.test_app)

        # Submit a review using marketplace API
        mock_review = MockReview()
        review_id = mk_api.submit_app_review(app['id'], mock_review.body, mock_review.rating)

        # Login into Marketplace
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        home_page.login(user="default")
        Assert.true(home_page.is_the_current_page)

        # Search for the test app and go to its details page
        search_page = home_page.header.search(self.test_app)
        details_page = search_page.results[0].click_name()
        Assert.true(details_page.is_the_current_page)

        Assert.true(details_page.is_edit_review_button_visible)
        Assert.equal(details_page.edit_review_button, "Edit Your Review")

        # Write a review
        edit_review = details_page.click_edit_review()
        mock_review = MockReview()
        details_page = edit_review.write_a_review(mock_review['rating'], mock_review['body'])

        # Check notification
        Assert.equal(details_page.notification_message, "Review updated successfully")

        # Go to reviews page and verify
        reviews = details_page.click_reviews_button()
        Assert.equal(reviews.logged_in_users_review.text, mock_review['body'])
        Assert.equal(reviews.logged_in_users_review.rating, mock_review['rating'])

        # Clean up
        mk_api.delete_app_review(review_id)

    @pytest.mark.xfail(reason="Need different apps for different tests for reviews. Issue https://github.com/mozilla/marketplace-tests/issues/320.")
    def test_that_checks_the_deletion_of_a_review(self, mozwebqa):
        """
        https://moztrap.mozilla.org/manage/case/648/
        """

        # Step 1 - Create new review
        mock_review = MockReview()
        mk_api = MarketplaceAPI(credentials=mozwebqa.credentials['api'])
        app = mk_api.get_app(self.test_app)
        review_id = mk_api.submit_app_review(app['id'], mock_review.body, mock_review.rating)

        # Step 2 - Login into Marketplace
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        home_page.login(user="default")
        home_page.wait_notification_box_not_visible()
        Assert.true(home_page.is_the_current_page)

        # Step 3 - Search for the test app and go to its details page
        search_page = home_page.header.search(self.test_app)
        details_page = search_page.results[0].click_name()
        Assert.true(details_page.is_the_current_page)

        # Step 4 - Go to reviews page
        reviews_page = details_page.click_reviews_button()

        # Step 5 - Delete review
        reviews = reviews_page.reviews[0]
        reviews.delete()
        Assert.true(reviews_page.notification_visible)
        Assert.equal(reviews_page.notification_message, "Review deleted")
        Assert.false(reviews.is_review_visible)
