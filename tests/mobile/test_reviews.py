#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from unittestzero import Assert
import pytest

from pages.mobile.home import Home
from mocks.mock_review import MockReview
from pages.mobile.add_review import AddReview
from pages.mobile.reviews import Reviews
from pages.mobile.details import Details
from persona_test_user import PersonaTestUser


class TestReviews():

    app_name = 'Twitter'

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
        add_review_box = AddReview(mozwebqa)
        add_review_box.write_a_review(mock_review['rating'], mock_review['body'])

        Assert.true(details_page.is_success_message_visible, "Review not added: %s" % details_page.success_message)
        Assert.equal(details_page.success_message, "Your review was posted")

        # Go to the reviews page and delete the review
        reviews_page = details_page.click_view_reviews()
        reviews = reviews_page.reviews[0]
        reviews.delete()
        Assert.true(reviews_page.is_success_message_visible, "Review not deleted: %s" % details_page.success_message)

        # After clicking back, current page is the app's details page.
        reviews_page.header.click_back()

        Assert.true(details_page.is_product_details_visible)
        Assert.equal(self.app_name, details_page.title)

    @pytest.mark.nondestructive
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

    def test_that_checks_the_addition_of_a_review(self, mozwebqa):
        new_user = PersonaTestUser().create_user()
        mock_review = MockReview()

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        # Create new user and login.
        settings_page = home_page.header.click_settings()
        settings_page.login(user=new_user)

        # Search for an app and go to it's details page.
        home_page.go_to_homepage()
        search_page = home_page.search_for(self.app_name)
        details_page = search_page.results[0].click_app()
        Assert.true(details_page.is_product_details_visible)

        # Write a review.
        details_page.click_write_review()
        add_review_box = AddReview(mozwebqa)
        details_page = add_review_box.write_a_review(mock_review['rating'], mock_review['body'])

        details_page.wait_for_page_to_load()
        Assert.true(details_page.is_success_message_visible, "Review not added: %s" % details_page.success_message)
        Assert.equal(details_page.success_message, "Your review was posted")

        # Go to the reviews page
        reviews_page = details_page.click_view_reviews()

        # Check review
        review = reviews_page.reviews[0]
        Assert.equal(review.rating, mock_review['rating'])
        Assert.contains(review.author, new_user['email'])
        Assert.equal(review.text, mock_review['body'])
