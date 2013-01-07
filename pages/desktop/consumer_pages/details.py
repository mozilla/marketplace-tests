#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from pages.desktop.consumer_pages.base import Base
from selenium.webdriver.common.by import By


class Details(Base):
    """APP details page
    https://marketplace-dev.allizom.org/en-US/app/ app name
    app_name => the name of the app displayed
    """

    _title_locator = (By.CSS_SELECTOR, '.info > h3')
    _purchase_locator = (By.CSS_SELECTOR, "section.product-details > div.actions > a.premium")
    _install_purchased_locator = (By.CSS_SELECTOR, "section.product-details > div.actions > a.premium.purchased.installing")
    _install_locator = (By.CSS_SELECTOR, "section.product-details > div.actions > a.install")
    _submit_review_link_locator = (By.ID, 'add-first-review')
    _image_locator = (By.CSS_SELECTOR, '.product-details.listing.expanded.c img[class="icon"]')
    _name_locator = (By.CSS_SELECTOR, '.info > h3')
    _app_dev_username_locator = (By.CSS_SELECTOR, '.author.lineclamp.vital')
    _application_description_locator = (By.CSS_SELECTOR, '.description')
    _image_preview_section_locator = (By.CSS_SELECTOR, '.slider')
    _support_email_locator = (By.CSS_SELECTOR, '.support-email > a')
    _app_site_locator = (By.CSS_SELECTOR, 'ul.c li:nth-child(2)')
    _privacy_policy_locator = (By.CSS_SELECTOR, '.c>li>a[href*="privacy"]')
    _expand_or_collapse_description_locator = (By.CSS_SELECTOR, '.show-toggle')
    _dots_locator = (By.CSS_SELECTOR, '.dot')
    _expanded_description_locator = (By.CSS_SELECTOR, ".collapsed")

    def __init__(self, testsetup, app_name=False):
        Base.__init__(self, testsetup)
        self.wait_for_ajax_on_page_finish()
        if app_name:
            self._page_title = "%s | Firefox Marketplace" % app_name
            self.app_name = app_name

    @property
    def _page_title(self):
        return '%s | Firefox Marketplace' % self.title

    @property
    def title(self):
        return self.selenium.find_element(*self._title_locator).text

    def is_app_available_for_purchase(self):
        return self.is_element_visible(*self._purchase_locator)

    @property
    def is_app_installing(self):
        return self.is_element_visible(*self._install_purchased_locator)

    @property
    def is_submit_review_link_visible(self):
        return self.is_element_visible(*self._submit_review_link_locator)

    @property
    def submit_review_link(self):
        return self.selenium.find_element(*self._submit_review_link_locator).text

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

    def click_submit_review(self):
        self.selenium.find_element(*self._submit_review_link_locator).click()
        from pages.desktop.consumer_pages.add_review import AddReview
        return AddReview(self.testsetup, self.app_name)

    @property
    def app_summary_text(self):
        return self.selenium.find_element(*self._application_description_locator).text

    @property
    def app_expanded_description_text(self):
        return self.selenium.find_element(*self._expanded_description_locator).text

    def expand_or_collapse_app_description(self):
        self.selenium.find_element(*self._expand_or_collapse_description_locator).click()

    @property
    def is_app_expanded_description_visible(self):
        return self.is_element_visible(*self._expanded_description_locator)

    @property
    def is_app_description_expanded(self):
        return 'More' in self.selenium.find_element(*self._expand_or_collapse_description_locator).get_attribute('data-toggle-text')
