#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import random

from datetime import datetime
from unittestzero import Assert


from pages.desktop.consumer_pages.home import Home
from pages.desktop.consumer_pages.details import Details


class TestReviews:

    def test_that_checks_the_addition_of_a_review(self, mozwebqa):
        test_app = "Test App (whateer1979)"

        # Step 1 - Login into Marketplace
        home_page = Home(mozwebqa)

        home_page.go_to_homepage()
        home_page.login()
        Assert.true(home_page.is_the_current_page)

        # Step 2 - Load the test app details page
        details_page = Details(mozwebqa, test_app)
        Assert.true(details_page.is_the_current_page)

        Assert.true(details_page.is_submit_review_link_visible)
        Assert.equal(details_page.submit_review_link, "Submit a Review")

        # Step 4 - Write a review
        body = 'Automatic app review by Selenium tests %s' % datetime.now()
        rating = random.randint(1, 5)
        review_page = self._write_a_review(details_page, test_app, rating, body)

        # Step 5 - Check review
        Assert.true(review_page.is_success_message_visible)
        Assert.equal(review_page.success_message, "Your review was successfully added!")
        review = review_page.reviews[0]
        Assert.equal(review.rating, rating)
        Assert.equal(review.author, mozwebqa.credentials['default']['name'])
        Assert.equal(review.text, body)

    def _write_a_review(self, details_page, test_app, rating, body):
        add_review_page = details_page.click_submit_review(test_app)
        Assert.true(add_review_page.is_the_current_page)

        add_review_page.set_review_rating(rating)
        add_review_page.enter_review_with_text(body)
        review_page = add_review_page.click_to_submit_review()

        return review_page
