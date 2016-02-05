#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By

from pages.mobile.base import Base


class Reviews(Base):
    """
    Page with all reviews of an app.
    """

    _review_list_locator = (By.CSS_SELECTOR, '.review')

    @property
    def _page_title(self):
        return 'Reviews | Firefox Marketplace'

    @property
    def reviews(self):
        """Returns review object with index."""
        return [self.Review(self.base_url, self.selenium, web_element) for web_element in self.selenium.find_elements(*self._review_list_locator)]

    class Review(Base):

            _review_text_locator = (By.CSS_SELECTOR, '.review-body')
            _review_rating_locator = (By.CSS_SELECTOR, '.stars')
            _review_author_locator = (By.CSS_SELECTOR, '.review-author')

            def __init__(self, base_url, selenium, element):
                Base.__init__(self, base_url, selenium)
                self._root_element = element

            @property
            def text(self):
                return self._root_element.find_element(*self._review_text_locator).text

            @property
            def rating(self):
                return int(self._root_element.find_element(*self._review_rating_locator).get_attribute('class')[-1])

            @property
            def author(self):
                return self._root_element.find_element(*self._review_author_locator).text
