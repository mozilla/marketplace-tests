# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.desktop.consumer_pages.base import Base
from pages.page import PageRegion


class Details(Base):
    """APP details page
    https://marketplace-dev.allizom.org/en-US/app/ app name
    app_name => the name of the app displayed
    """

    _title_locator = (By.CSS_SELECTOR, '.info > h3')
    _install_purchased_locator = (By.CSS_SELECTOR, 'section.product-details > div.actions > a.premium.purchased.installing')
    _install_locator = (By.CSS_SELECTOR, '.button.mkt-app-button.install')
    _image_locator = (By.CSS_SELECTOR, '.mkt-tile .mkt-app-heading .icon')
    _name_locator = (By.CSS_SELECTOR, '.info > h3')
    _support_email_locator = (By.CSS_SELECTOR, '.support-email > a')
    _app_site_locator = (By.CSS_SELECTOR, '.support-url > a')
    _app_dev_username_locator = (By.CSS_SELECTOR, '.author')
    _application_description_locator = (By.CSS_SELECTOR, '.description')
    _image_preview_section_locator = (By.CSS_SELECTOR, 'div.previews-tray[data-previews-desktop] .previews-slider')
    _content_ratings_button_locator = (By.CSS_SELECTOR, '.content-ratings-wrapper .content-ratings-button-wrap .button')
    _content_ratings_image_locator = (By.CSS_SELECTOR, '.content-rating img')
    _privacy_policy_locator = (By.CSS_SELECTOR, '#footer a[href*="privacy"]')
    _dots_locator = (By.CSS_SELECTOR, '.dot')
    _expanded_description_locator = (By.CSS_SELECTOR, '.collapsed')
    _review_button_locator = (By.CSS_SELECTOR, '.button.review-button')
    _first_review_body_locator = (By.CSS_SELECTOR, '.reviews-wrapper li:nth-child(1) .review-body')
    _first_review_locator = (By.CSS_SELECTOR, '.reviews-wrapper li:nth-child(1)')
    _reviews_button_locator = (By.CSS_SELECTOR, '.review-buttons li:nth-child(2) .button')
    _report_abuse_button_locator = (By.CSS_SELECTOR, '.button.abuse')
    _report_abuse_box_locator = (By.CSS_SELECTOR, '.abuse-form')
    _app_price_locator = (By.CSS_SELECTOR, '.button.mkt-app-button.install > em')

    def __init__(self, testsetup, app_name=None):
        Base.__init__(self, testsetup)
        self.wait_for_page_to_load()
        self.app_name = app_name

    @property
    def _page_title(self):
        app_name = self.app_name or self.title
        return '%s | Firefox Marketplace' % app_name

    @property
    def title(self):
        return self.selenium.find_element(*self._title_locator).text

    @property
    def is_app_installing(self):
        return self.is_element_visible(*self._install_purchased_locator)

    def wait_for_review_button_visible(self):
        self.wait_for_element_visible(*self._review_button_locator)

    @property
    def is_support_email_visible(self):
        return self.is_element_visible(*self._support_email_locator)

    @property
    def is_app_site_visible(self):
        return self.is_element_visible(*self._app_site_locator)

    @property
    def review_button_text(self):
        return self.selenium.find_element(*self._review_button_locator).text

    @property
    def name(self):
        return self.selenium.find_element(*self._name_locator).text

    @property
    def is_app_dev_username_visible(self):
        return self.is_element_visible(*self._app_dev_username_locator)

    @property
    def is_image_visible(self):
        return self.is_element_visible(*self._image_locator)

    @property
    def is_application_description_visible(self):
        return self.is_element_visible(*self._application_description_locator)

    @property
    def is_image_preview_section_visible(self):
        return self.is_element_visible(*self._image_preview_section_locator)

    @property
    def dot_count(self):
        return len(self.selenium.find_elements(*self._dots_locator))

    @property
    def is_privacy_policy_link_visible(self):
        return self.is_element_visible(*self._privacy_policy_locator)

    @property
    def is_install_button_visible(self):
        return self.is_element_visible(*self._install_locator)

    def click_install_button(self):
        self.selenium.find_element(*self._install_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(lambda s: 'purchasing' in self.app_status)
        from pages.desktop.payment.payment_popup import Payment
        return Payment(self.testsetup)

    def click_review_button(self, edit_review=False):
        review_button = self.selenium.find_element(*self._review_button_locator)
        self.scroll_to_element(review_button)
        review_button.click()
        if not edit_review:
            from pages.desktop.consumer_pages.add_review import AddReview
            return AddReview(self.testsetup)
        from pages.desktop.consumer_pages.edit_review import EditReview
        return EditReview(self.testsetup)

    def wait_for_app_purchased(self):
        WebDriverWait(self.selenium, self.timeout).until(lambda s: 'purchased' in self.app_status)

    @property
    def app_summary_text(self):
        return self.selenium.find_element(*self._application_description_locator).text

    @property
    def app_expanded_description_text(self):
        return self.selenium.find_element(*self._expanded_description_locator).text

    @property
    def is_app_expanded_description_visible(self):
        return self.is_element_visible(*self._expanded_description_locator)

    @property
    def is_app_description_expanded(self):
        return 'More' in self.selenium.find_element(*self._expand_or_collapse_description_locator).get_attribute('data-toggle-text')

    @property
    def first_review_rating(self):
        self.wait_for_element_visible(*self._first_review_locator)
        return int(self.selenium.find_element(*self._first_review_locator).get_attribute('data-rating'))

    @property
    def first_review_body(self):
        self.wait_for_element_visible(*self._first_review_body_locator)
        return self.selenium.find_element(*self._first_review_body_locator).text

    def click_all_reviews_button(self):
        self.selenium.find_element(*self._reviews_button_locator).click()
        from pages.desktop.consumer_pages.reviews import Reviews
        return Reviews(self.testsetup)

    @property
    def is_report_abuse_button_visible(self):
        return self.is_element_visible(*self._report_abuse_button_locator)

    def click_report_abuse_button(self):
        report_abuse_button = self.selenium.find_element(*self._report_abuse_button_locator)
        self.scroll_to_element(report_abuse_button)
        report_abuse_button.click()
        return self.report_abuse_box

    @property
    def report_abuse_box(self):
        report_abuse_box = self.find_element(*self._report_abuse_box_locator)
        return self.ReportAbuseRegion(self.testsetup, report_abuse_box)

    def click_content_ratings_button(self):
        content_ratings_button = self.selenium.find_element(*self._content_ratings_button_locator)
        self.scroll_to_element(content_ratings_button)
        content_ratings_button.click()
        return GlobalRatings(self.testsetup)

    def wait_for_ratings_image_visible(self):
        self.wait_for_element_visible(*self._content_ratings_image_locator)

    @property
    def price_text(self):
        return self.selenium.find_element(*self._app_price_locator).text

    @property
    def app_status(self):
        self.wait_for_element_visible(*self._install_locator)
        return self.selenium.find_element(*self._install_locator).get_attribute('class')

    class ReportAbuseRegion(PageRegion):

        _report_button = (By.CSS_SELECTOR, 'button[type="submit"]')
        _report_textarea = (By.CSS_SELECTOR, '.abuse-form > textarea')

        @property
        def is_visible(self):
            return self.is_element_visible(*self._report_button)

        @property
        def is_report_button_enabled(self):
            return self.find_element(*self._report_button).is_enabled()

        def click_report_button(self):
            self.find_element(*self._report_button).click()

        def insert_text(self, text):
            self.find_element(*self._report_textarea).send_keys(text)


class GlobalRatings(Base):

        _page_title = 'IARC Ratings Guide | International Age Rating Coalition'

        _content_ratings_table_locator = (By.CSS_SELECTOR, '.ratingsguide')

        def __init__(self, testsetup):
            Base.__init__(self, testsetup)

            if self.selenium.title != self._page_title:
                for handle in self.selenium.window_handles:
                    self.selenium.switch_to_window(handle)
                    WebDriverWait(self.selenium, self.timeout).until(lambda s: s.title)
            else:
                raise Exception('Page has not loaded')

        @property
        def is_ratings_table_visible(self):
            return self.is_element_visible(*self._content_ratings_table_locator)
