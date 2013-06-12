#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By

from pages.desktop.consumer_pages.base import Base


class AddReview(Base):

    _star_rating_locator = (By.CSS_SELECTOR, '.ratingwidget.stars.large.stars-0 > label')
    _add_review_input_field_locator = (By.CSS_SELECTOR, '.add-review-form p #id_body')
    _submit_review_button_locator = (By.CSS_SELECTOR, '.two-up > button[type="submit"]')

    _add_review_box = (By.ID, 'feedback-form')

    def set_review_rating(self, rating):
        self.selenium.find_element(self._star_rating_locator[0],
                                             '%s[data-stars="%s"]' % (self._star_rating_locator[1], rating)).click()

    def enter_review_with_text(self, text):
        self.selenium.find_element(*self._add_review_input_field_locator).send_keys(text)

    def write_a_review(self, rating, body):
        self.set_review_rating(rating)
        self.enter_review_with_text(body)
        self.selenium.find_element(*self._submit_review_button_locator).click()
        from pages.desktop.consumer_pages.details import Details
        return Details(self.testsetup)

    @property
    def is_review_box_visible(self):
        return self.is_element_visible(*self._add_review_box)
