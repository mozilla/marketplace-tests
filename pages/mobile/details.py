# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.page import PageRegion
from pages.mobile.base import Base


class Details(Base):

    _title_locator = (By.CSS_SELECTOR, '.mkt-header--title')
    _write_review_locator = (By.CSS_SELECTOR, '.review-button')
    _view_reviews_locator = (By.CSS_SELECTOR, '.review-buttons li:nth-child(2) .button')
    _product_details_locator = (By.CSS_SELECTOR, '.main.full.app-header.previews-expanded > div')
    _app_icon_locator = (By.CSS_SELECTOR, '.mkt-tile .icon')
    _author_locator = (By.CSS_SELECTOR, '.author')
    _rating_header_locator = (By.CLASS_NAME, 'rating-link')
    _app_description_locator = (By.CLASS_NAME, 'description')
    _rating_count_locator = (By.CSS_SELECTOR, '.reviews-summary-large > p')
    _reviews_locator = (By.CSS_SELECTOR, '.review.c')
    _app_not_rated_yet_locator = (By.CLASS_NAME, 'not-rated')

    # Support buttons
    _support_email_locator = (By.CSS_SELECTOR, '.support-email > a')
    _support_site_locator = (By.CSS_SELECTOR, '.support-url > a')
    _homepage_locator = (By.CSS_SELECTOR, '.homepage > a')
    _privacy_policy_locator = (By.CSS_SELECTOR, '.privacy-policy > a')
    _report_abuse_locator = (By.CSS_SELECTOR, '.button.abuse')

    support_buttons_list = [_support_email_locator, _support_site_locator,
                            _homepage_locator, _privacy_policy_locator, _report_abuse_locator]

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
    def is_author_visible(self):
        return self.is_element_visible(*self._author_locator)

    @property
    def is_rating_visible(self):
        return self.is_element_visible(*self._rating_header_locator)

    def click_write_review(self):
        write_review_button = self.selenium.find_element(*self._write_review_locator)
        WebDriverWait(self.selenium, self.timeout).until(lambda s: write_review_button.is_displayed())
        self.scroll_to_element(write_review_button)
        write_review_button.click()
        from pages.mobile.add_review import AddReview
        return AddReview(self.base_url, self.selenium)

    def click_view_reviews(self):
        view_reviews_button = self.selenium.find_element(*self._view_reviews_locator)
        WebDriverWait(self.selenium, self.timeout).until(lambda s: view_reviews_button.is_displayed())
        self.scroll_to_element(view_reviews_button)
        view_reviews_button.click()
        from pages.mobile.reviews import Reviews
        return Reviews(self.base_url, self.selenium)

    def go_to_reviews_page(self):
        self.selenium.get('%s/ratings' % self.selenium.current_url.split('?')[0])
        from pages.mobile.reviews import Reviews
        return Reviews(self.base_url, self.selenium)

    @property
    def is_app_icon_present(self):
        return self.is_element_present(*self._app_icon_locator)

    @property
    def is_description_visible(self):
        return self.is_element_visible(*self._app_description_locator)

    @property
    def reviews_count(self):
        reviews_count = self.selenium.find_element(*self._rating_count_locator).text
        a = reviews_count.split()[0]
        return int(a.replace(',', ''))

    @property
    def reviews(self):
        return [self.Review(self.base_url, self.selenium, web_element)
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

    class Review(PageRegion):

        _name_locator = (By.CSS_SELECTOR, '.review-author')

        @property
        def name(self):
            return self.find_element(*self._name_locator).text

        @property
        def is_visible(self):
            return self.find_element(*self._name_locator).is_displayed()

        @property
        def review_id(self):
            return self._root_element.get_attribute('data-report-uri').split('/')[5]
