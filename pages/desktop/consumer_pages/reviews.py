#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By

from pages.desktop.consumer_pages.base import Base


class Reviews(Base):
    """
    Page with all reviews of an app.
    https://marketplace-dev.allizom.org/en-US/app/app-name/reviews/
    """

    _review_locator = (By.CSS_SELECTOR, '.review')

    def __init__(self, testsetup, app_name=False):
        Base.__init__(self, testsetup)
        self.wait_for_page_to_load()
        if app_name:
            self._page_title = "Reviews for %s | Firefox Marketplace" % app_name

    @property
    def reviews(self):
        """Returns review object with index."""
        return [self.Review(self.testsetup, web_element)
                for web_element in self.selenium.find_elements(*self._review_locator)]

    def get_review_for_user(self, user_name):
        for review in self.reviews:
            if review.author == user_name:
                break
        else:
            raise Exception('Could not find review for user: %s.' % user_name)

        return review

    def is_review_for_user_present(self, user_name):
        for review in self.reviews:
            if review.author == user_name:
                return True
        return False

    class Review(Base):

        _review_text_locator = (By.CSS_SELECTOR, '.review-body')
        _review_rating_locator = (By.CSS_SELECTOR, 'span.stars > span[itemprop=reviewRating]')
        _review_author_locator = (By.CSS_SELECTOR, '.review-author')
        _delete_review_locator = (By.CSS_SELECTOR, '.delete')
        _edit_review_locator = (By.CSS_SELECTOR, '.edit')

        def __init__(self, testsetup, element):
            Base.__init__(self, testsetup)
            self._root_element = element

        @property
        def text(self):
            return self._root_element.find_element(*self._review_text_locator).text

        @property
        def rating(self):
            return int(self._root_element.get_attribute('data-rating'))

        @property
        def author(self):
            return self._root_element.find_element(*self._review_author_locator).text

        def delete(self):
            self._root_element.find_element(*self._delete_review_locator).click()
