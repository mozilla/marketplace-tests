#!/usr/bin/env python

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
    _purchase_locator = (By.CSS_SELECTOR, 'section.product-details > div.actions > a.premium')
    _install_purchased_locator = (By.CSS_SELECTOR, 'section.product-details > div.actions > a.premium.purchased.installing')
    _install_locator = (By.CSS_SELECTOR, '.button.product.install')
    _image_locator = (By.CSS_SELECTOR, '.product-details.listing.expanded.c img[class="icon"]')
    _name_locator = (By.CSS_SELECTOR, '.info > h3')
    _app_dev_username_locator = (By.CSS_SELECTOR, '.author')
    _application_description_locator = (By.CSS_SELECTOR, '.description')
    _image_preview_section_locator = (By.CSS_SELECTOR, '.slider')
    _support_email_locator = (By.CSS_SELECTOR, '.support-email > a')
    _content_ratings_button_locator = (By.CSS_SELECTOR, '.content-ratings-wrapper .button.support')
    _content_ratings_image_locator = (By.CSS_SELECTOR, '.content-rating.c img')
    _app_site_locator = (By.CSS_SELECTOR, '.support-url > a')
    _privacy_policy_locator = (By.CSS_SELECTOR, '#footer a[href*="privacy"]')
    _dots_locator = (By.CSS_SELECTOR, '.dot')
    _expanded_description_locator = (By.CSS_SELECTOR, '.collapsed')
    _write_review_button_locator = (By.ID, 'add-review')
    _edit_review_button_locator = (By.ID, 'edit-review')
    _first_review_body_locator = (By.CSS_SELECTOR, 'li:first-child .body')
    _first_review_locator = (By.CSS_SELECTOR, 'li:first-child .review-inner > span')
    _reviews_button_locator = (By.CSS_SELECTOR, '.button.average-rating')
    _report_abuse_button_locator = (By.CSS_SELECTOR, '.abuse > a')
    _report_abuse_box_locator = (By.CSS_SELECTOR, '.report-abuse')

    def __init__(self, testsetup, app_name=False, first_access=False):
        Base.__init__(self, testsetup)
        if first_access:
            self.wait_for_page_to_load()
        if app_name:
            self._page_title = "%s | Firefox Marketplace" % app_name
            self.app_name = app_name
        else:
            self._page_title = "%s | Firefox Marketplace" % self.title

    @property
    def title(self):
        return self.selenium.find_element(*self._title_locator).text

    @property
    def is_app_available_for_purchase(self):
        return self.is_element_visible(*self._purchase_locator)

    @property
    def is_app_installing(self):
        return self.is_element_visible(*self._install_purchased_locator)

    def wait_write_review_button_visible(self):
        self.wait_for_element_visible(*self._write_review_button_locator)

    @property
    def is_edit_review_button_visible(self):
        return self.is_element_visible(*self._edit_review_button_locator)

    @property
    def write_review_button(self):
        return self.selenium.find_element(*self._write_review_button_locator).text

    @property
    def edit_review_button(self):
        return self.selenium.find_element(*self._edit_review_button_locator).text

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
    def is_support_email_visible(self):
        return self.is_element_visible(*self._support_email_locator)

    @property
    def is_app_site_visible(self):
        return self.is_element_visible(*self._app_site_locator)

    @property
    def is_privacy_policy_link_visible(self):
        return self.is_element_visible(*self._privacy_policy_locator)

    @property
    def is_install_button_visible(self):
        return self.is_element_visible(*self._install_locator)

    def click_write_review(self):
        self.scroll_to_element(*self._write_review_button_locator)
        self.selenium.find_element(*self._write_review_button_locator).click()
        from pages.desktop.consumer_pages.add_review import AddReview
        return AddReview(self.testsetup)

    def click_edit_review(self):
        self.scroll_to_element(*self._edit_review_button_locator)
        self.selenium.find_element(*self._edit_review_button_locator).click()
        from pages.desktop.consumer_pages.edit_review import EditReview
        return EditReview(self.testsetup)

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
        return int(self.selenium.find_element(*self._first_review_locator).get_attribute('class')[-1])

    @property
    def first_review_body(self):
        self.wait_for_element_visible(*self._first_review_body_locator)
        return self.selenium.find_element(*self._first_review_body_locator).text

    def click_reviews_button(self):
        self.selenium.find_element(*self._reviews_button_locator).click()
        from pages.desktop.consumer_pages.reviews import Reviews
        return Reviews(self.testsetup)

    @property
    def is_report_abuse_button_visible(self):
        return self.is_element_visible(*self._report_abuse_button_locator)

    def click_report_abuse_button(self):
        self.scroll_to_element(*self._report_abuse_button_locator)
        self.selenium.find_element(*self._report_abuse_button_locator).click()
        return self.report_abuse_box

    @property
    def report_abuse_box(self):
        report_abuse_box = self.find_element(*self._report_abuse_box_locator)
        return self.ReportAbuseRegion(self.testsetup, report_abuse_box)

    def click_content_ratings_button(self):
        self.scroll_to_element(*self._content_ratings_button_locator)
        self.find_element(*self._content_ratings_button_locator).click()
        return GlobalRatings(self.testsetup)

    @property
    def is_ratings_image_visible(self):
        return self.is_element_visible(*self._content_ratings_image_locator)

    def login_with_user_from_other_pages(self, user="default"):
        from pages.fxa import FirefoxAccounts
        fxa = FirefoxAccounts(self.testsetup)
        fxa.login_user(user)


    class ReportAbuseRegion(PageRegion):

        _report_button = (By.CSS_SELECTOR, '.button')
        _report_textarea = (By.CSS_SELECTOR, '.abuse-form > p > textarea')

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

        _content_ratings_table_locator = (By.CSS_SELECTOR, '.ratings')

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
