# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from tests.base_test import BaseTest
from mocks.mock_review import MockReview
from pages.desktop.consumer_pages.home import Home


class TestReviews(BaseTest):

    def _create_review(self, mozwebqa, user):
        # Step 1 - Login into Marketplace
        mock_review = MockReview()
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        home_page.header.click_sign_in()
        home_page.login(user['email'], user['password'])
        assert home_page.is_the_current_page

        # Step 2 - Search for the test app and go to its details page
        app_name = self._take_first_free_app_name(mozwebqa)
        details_page = home_page.header.search_and_click_on_app(app_name)
        assert details_page.is_the_current_page

        details_page.wait_for_review_button_visible()
        assert 'Write a review' == details_page.review_button_text

        # Step 3 - Write a review
        add_review_box = details_page.click_review_button()
        details_page = add_review_box.write_a_review(mock_review['rating'], mock_review['body'])

        # Step 4 - Check review
        assert mock_review['rating'] == details_page.first_review_rating
        assert mock_review['body'] == details_page.first_review_body

        return app_name

    @pytest.mark.sanity
    def test_that_checks_the_addition_of_a_review(self, mozwebqa, new_user):
        """The entire test is implemented in _create_review so it can
           be reused by other tests.
        """
        self._create_review(mozwebqa, new_user)

    def test_add_review_after_sign_in_from_details_page(self, mozwebqa, new_user):
        # Go to Marketplace Home page
        mock_review = MockReview()
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        assert home_page.is_the_current_page

        # Search for the test app and go to its details page
        search_term = self._take_first_free_app_name(mozwebqa)
        details_page = home_page.header.search_and_click_on_app(search_term)
        assert details_page.is_the_current_page
        assert 'Sign in to review' == details_page.review_button_text

        # Login
        add_review_box = details_page.click_review_button()
        details_page.login(new_user['email'], new_user['password'])

        add_review_box.write_a_review(mock_review['rating'], mock_review['body'])
        assert mock_review['rating'] == details_page.first_review_rating
        assert mock_review['body'] == details_page.first_review_body

    @pytest.mark.sanity
    def test_that_checks_the_editing_of_a_review(self, mozwebqa, new_user):
        # Create the review to be edited
        app_name = self._create_review(mozwebqa, new_user)

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        details_page = home_page.header.search_and_click_on_app(app_name)
        assert details_page.is_the_current_page

        details_page.wait_for_review_button_visible()
        assert 'Edit your review' == details_page.review_button_text

        # Edit the review
        edit_review = details_page.click_review_button(edit_review=True)
        mock_review = MockReview()
        details_page = edit_review.write_a_review(mock_review['rating'], mock_review['body'])

        # Go to reviews page and verify
        reviews_page = details_page.click_all_reviews_button()
        review = reviews_page.get_review_for_user(new_user['name'])
        assert mock_review['body'] == review.text
        assert mock_review['rating'] == review.rating

    @pytest.mark.sanity
    def test_that_checks_the_deletion_of_a_review(self, mozwebqa, new_user):
        """
        https://moztrap.mozilla.org/manage/case/648/
        """
        # Create the review to be deleted
        app_name = self._create_review(mozwebqa, new_user)

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        details_page = home_page.header.search_and_click_on_app(app_name)
        assert details_page.is_the_current_page

        reviews_page = details_page.click_all_reviews_button()
        review = reviews_page.get_review_for_user(new_user['name'])
        review.delete()
        details_page.wait_for_notification(
            'This review has been successfully deleted')
        assert not reviews_page.is_review_for_user_present(new_user['name'])
