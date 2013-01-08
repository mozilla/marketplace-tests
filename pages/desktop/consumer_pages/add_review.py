#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By

from pages.desktop.consumer_pages.base import Base


class AddReview(Base):

    _star_rating_locator = (By.CSS_SELECTOR, '.ratingwidget.stars.large.stars-0 > label')
    _add_review_input_field_locator = (By.ID, 'id_body')
    _submit_review_button_locator = (By.CSS_SELECTOR, '#edit-review button')

    _add_review_box = (By.ID, 'feedback-form')

    def __init__(self, testsetup, app_name=False):
        Base.__init__(self, testsetup)
        if app_name:
            self._page_title = "Add a review for %s | Firefox Marketplace" % app_name

    def set_review_rating(self, rating):
        self.selenium.find_element(self._star_rating_locator[0],
                                             '%s[data-stars="%s"]' % (self._star_rating_locator[1], rating)).click()

    def enter_review_with_text(self, text):
        self.selenium.find_element(*self._add_review_input_field_locator).send_keys(text)

    def click_to_save_review(self):
        self.selenium.find_element(*self._submit_review_button_locator).click()
        from pages.desktop.consumer_pages.reviews import Reviews
        return Reviews(self.testsetup)

    @property
    def is_review_box_visible(self):
        return self.is_element_visible(*self._add_review_box)
