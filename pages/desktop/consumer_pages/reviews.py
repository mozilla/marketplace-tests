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

    _review_locator = (By.CSS_SELECTOR, '.ratings-placeholder-inner li')
    _success_notification_locator = (By.ID, 'notification-content')

    def __init__(self, testsetup, app_name=False):
        Base.__init__(self, testsetup)
        self.wait_for_page_to_load()
        if app_name:
            self._page_title = "Reviews for %s | Firefox Marketplace" % app_name

    @property
    def reviews(self):
        """Returns review object with index."""
        return [self.ReviewSnippet(self.testsetup, web_element) for web_element in self.selenium.find_elements(*self._review_locator)]

    @property
    def is_success_message_visible(self):
        return self.is_element_visible(*self._success_notification_locator)

    @property
    def success_message(self):
        return self.selenium.find_element(*self._success_notification_locator).text

    class ReviewSnippet(Base):

        _review_text_locator = (By.CSS_SELECTOR, '.body')
        _review_rating_locator = (By.CSS_SELECTOR, 'span.stars')
        _review_author_locator = (By.CSS_SELECTOR, '.byline > strong')
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
            return int(self._root_element.find_element(*self._review_rating_locator).text.split()[1])

        @property
        def author(self):
            return self._root_element.find_element(*self._review_author_locator).text

        def delete(self):
            self._root_element.find_element(*self._delete_review_locator).click()
            self.wait_for_page_to_load()

        @property
        def is_review_visible(self):
            return self.is_element_visible(*self._review_text_locator)
