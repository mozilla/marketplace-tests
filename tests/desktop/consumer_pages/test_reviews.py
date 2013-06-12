#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert
from selenium import webdriver

from persona_test_user import PersonaTestUser
from mocks.mock_review import MockReview
from pages.desktop.consumer_pages.home import Home


class TestReviews:

    test_app = 'Twitter'

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
        Assert.true(details_page.is_success_message_visible, "Review not added: %s" % details_page.success_message)
        Assert.equal(details_page.success_message, "Your review was posted")
        Assert.equal(details_page.first_review_rating, mock_review['rating'])
        Assert.equal(details_page.first_review_body, mock_review['body'])

    @pytest.mark.skipif("webdriver.__version__ >= '2.32.0'", reason='Issue 5499: is_displyed() returns True, even if the element is not visible to the user')
    def test_that_checks_the_deletion_of_a_review(self, mozwebqa):
        """
        https://moztrap.mozilla.org/manage/case/648/
        """

        # Step 1 - Login into Marketplace
        mock_review = MockReview()
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        home_page.login()
        Assert.true(home_page.is_the_current_page)

        # Step 2 - Search for the test app and go to its details page
        search_page = home_page.header.search(self.test_app)
        details_page = search_page.results[0].click_name()
        Assert.true(details_page.is_the_current_page)
        Assert.true(details_page.is_write_review_button_visible)

        # Step 3 - Write a review
        add_review_box = details_page.click_write_review()
        details_page = add_review_box.write_a_review(mock_review['rating'], mock_review['body'])

        # Step 4 - Check review
        Assert.true(details_page.is_success_message_visible)

        # Step 5 - Go to reviews page
        reviews_page = details_page.click_reviews_button()

        # Step 6 - Delete review
        reviews = reviews_page.reviews[0]
        reviews.delete()
        Assert.true(reviews_page.is_success_message_visible)
        Assert.equal(reviews_page.success_message, "Your review was deleted")
        Assert.false(reviews.is_review_visible)
