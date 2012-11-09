#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from unittestzero import Assert

from pages.mobile.home import Home
from mocks.mock_review import MockReview
from pages.mobile.add_review import AddReview


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
        Assert.true(details_page.is_the_current_page)

        # Write a review.
        details_page.click_write_review()
        details_page.login_with_user_from_other_pages(user="default")
        add_review_page = AddReview(mozwebqa)
        review_page = add_review_page.write_a_review(mock_review['rating'], mock_review['body'])

        Assert.true(review_page.is_succesful_message, "Review not added: %s" % review_page.notification_message)

        # After clicking back, current page is the app's details page.
        review_page.header.click_back()
        Assert.true(details_page.is_the_current_page)
        Assert.equal(self.app_name, details_page.title)
