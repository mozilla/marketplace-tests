#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import random

from datetime import datetime
from unittestzero import Assert

from mocks.mock_user import MockUser
from pages.desktop.consumer_pages.home import Home


class TestReviews:

    test_app = "Bimmer"

    def test_that_checks_the_addition_of_a_review(self, mozwebqa):

        # Step 1 - Login into Marketplace
        user = MockUser()
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        home_page.create_new_user(user)
        home_page.login(user)
        Assert.true(home_page.is_the_current_page)

        # Step 2 - Search for the test app and go to its details page
        search_page = home_page.header.search(self.test_app)
        details_page = search_page.results[0].click_name()
        Assert.true(details_page.is_the_current_page)

        Assert.true(details_page.is_write_review_link_visible)
        Assert.equal(details_page.writet_review_link, "Write a Review")

        # Step 3 - Write a review
        body = 'Automatic app review by Selenium tests %s' % datetime.now()
        rating = random.randint(1, 5)
        add_review_page = details_page.click_write_review()
        review_page = add_review_page.write_a_review(rating, body)

        # Step 4 - Check review
        Assert.true(review_page.is_success_message_visible)
        Assert.equal(review_page.success_message, "Your review was successfully added!")
        review = review_page.reviews[0]
        Assert.equal(review.rating, rating)
        Assert.equal(review.author, user.name)
        Assert.equal(review.text, body)

    def test_that_checks_the_deletion_of_a_review(self, mozwebqa):
        """
        https://moztrap.mozilla.org/manage/case/648/
        """
        # Step 1 - Login into Marketplace
        user = MockUser()
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        home_page.create_new_user(user)
        home_page.login(user)
        Assert.true(home_page.is_the_current_page)

        # Step 2 - Search for the test app and go to its details page
        search_page = home_page.header.search(self.test_app)
        details_page = search_page.results[0].click_name()
        Assert.true(details_page.is_the_current_page)

        Assert.true(details_page.is_write_review_link_visible)

        # Step 3 - Write a review
        body = 'Automatic app review by Selenium tests %s' % datetime.now()
        rating = random.randint(1, 5)
        add_review_page = details_page.click_write_review()
        reviews_page = add_review_page.write_a_review(rating, body)

        # Step 4 - Check review
        Assert.true(reviews_page.is_success_message_visible)

        # Step 5 - Delete review
        review = reviews_page.reviews[0]
        review.delete()
        Assert.true(reviews_page.is_success_message_visible)
        Assert.equal(reviews_page.success_message, "Your review was successfully deleted!")
        Assert.false(review.is_review_visible)
