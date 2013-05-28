#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.page import PageRegion
from pages.mobile.base import Base


class Details(Base):

    _title_locator = (By.CSS_SELECTOR, 'div.info > h3')
    _write_review_locator = (By.ID, 'add-review')
    _view_reviews_locator = (By.CSS_SELECTOR, '.button.alt.average-rating')
    _product_details_locator = (By.CSS_SELECTOR, 'section.product-details')
    _app_icon_locator = (By.CSS_SELECTOR, '.product .icon')
    _author_locator = (By.CSS_SELECTOR, '.author.lineclamp.vital')
    _rating_header_locator = (By.CLASS_NAME, 'rating_link')
    _app_description_locator = (By.CLASS_NAME, 'description')
    _more_less_locator = (By.CLASS_NAME, 'show-toggle')
    _rating_count_locator = (By.CSS_SELECTOR, '.average-rating span:nth-child(1)')
    _success_notification_locator = (By.ID, 'notification-content')

    _reviews_locator = (By.CSS_SELECTOR, '#reviews-detail li')
    _support_section_buttons_locator = (By.CSS_SELECTOR, '#support .c li')
    _app_not_rated_yet_locator = (By.CLASS_NAME, 'not-rated')

    @property
    def _page_title(self):
        return '%s | Firefox Marketplace' % self.title

    @property
    def is_product_details_visible(self):
        return self.is_element_visible(*self._product_details_locator)

    @property
    def title(self):
        return self.selenium.find_element(*self._title_locator).text

    @property
    def is_success_message_visible(self):
        return self.is_element_visible(*self._success_notification_locator)

    @property
    def success_message(self):
        return self.selenium.find_element(*self._success_notification_locator).text

    @property
    def is_author_visible(self):
        return self.is_element_visible(*self._author_locator)

    @property
    def is_rating_visible(self):
        return self.is_element_visible(*self._rating_header_locator)

    def click_write_review(self):
        self.scroll_to_element(*self._write_review_locator)
        self.selenium.find_element(*self._write_review_locator).click()

    def click_view_reviews(self):
        self.scroll_to_element(*self._view_reviews_locator)
        self.selenium.find_element(*self._view_reviews_locator).click()
        from pages.mobile.reviews import Reviews
        return Reviews(self.testsetup)

    def login_with_user_from_other_pages(self, user="default"):
            from browserid.pages.sign_in import SignIn
            bid_login = SignIn(self.selenium, self.timeout)
            self.selenium.execute_script('localStorage.clear()')
            credentials = self.testsetup.credentials[user]
            bid_login.sign_in(credentials['email'], credentials['password'])

    @property
    def is_app_icon_present(self):
        return self.is_element_present(*self._app_icon_locator)

    def click_more_button(self):
        if self.is_element_present(*self._more_less_locator):
            self.selenium.find_element(*self._more_less_locator).click()

    @property
    def is_description_visible(self):
        return self.is_element_visible(*self._app_description_locator)

    @property
    def reviews_count(self):
        reviews_count = self.selenium.find_element(*self._rating_count_locator).text
        return int(reviews_count.split()[0])

    @property
    def reviews(self):
        return [self.Review(self.testsetup, web_element)
                for web_element in self.selenium.find_elements(*self._reviews_locator)]

    @property
    def is_write_a_review_button_visible(self):
        return self.is_element_visible(*self._write_review_locator)

    @property
    def is_app_rated(self):
        return not self.is_element_present(*self._app_not_rated_yet_locator)

    @property
    def app_not_rated_text(self):
        return self.selenium.find_element(*self._app_not_rated_yet_locator).text

    @property
    def support_buttons(self):
        return [self.SupportButton(self.testsetup, web_element)
                for web_element in self.selenium.find_elements(*self._support_section_buttons_locator)]

    class Review(PageRegion):
            _name_locator = (By.CSS_SELECTOR, 'strong')

            @property
            def name(self):
                return self.find_element(*self._name_locator).text

            @property
            def is_visible(self):
                return self.find_element(*self._name_locator).is_displayed()

    class SupportButton(PageRegion):
            _name_locator = (By.CSS_SELECTOR, 'a')

            @property
            def name(self):
                return self.find_element(*self._name_locator).text

            @property
            def is_visible(self):
                return self.find_element(*self._name_locator).is_displayed()
