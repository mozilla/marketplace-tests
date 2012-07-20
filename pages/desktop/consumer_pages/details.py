#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from pages.desktop.consumer_pages.base import Base
from selenium.webdriver.common.by import By

from pages.page import Page


class Details(Base):
    """APP details page
    https://marketplace-dev.allizom.org/en-US/app/ app name
    app_name => the name of the app displayed
    """
    _purchase_locator = (By.CSS_SELECTOR, "section.product-details > div.actions > a.premium")
    _install_purchased_locator = (By.CSS_SELECTOR, "section.product-details > div.actions > a.premium.purchased.installing")
    _install_locator = (By.CSS_SELECTOR, "section.product-details > div.actions > a.install")
    _submit_review_link_locator = (By.ID, 'add-first-review')
    _statistics_link_locator = (By.CSS_SELECTOR, "p.view-stats a.arrow")
    _image_locator = (By.CSS_SELECTOR, ".product-details > .visual > img")
    _name_locator = (By.CSS_SELECTOR, ".product-details .vitals.c > h1.oneline")
    _app_dev_username_locator = (By.CSS_SELECTOR, ".vitals.c > .authors.oneline.wide > a")
    _weekly_downloads_locator = (By.CSS_SELECTOR, ".details > .vitals > .vital.downloads")
    _section_device_icon_locator = (By.CSS_SELECTOR, ".vitals.c > .device-list.c > ul")
    _application_description_locator = (By.CSS_SELECTOR, ".description > .summary")
    _image_preview_section_locator = (By.CSS_SELECTOR, ".previews.slider.full > .alt-slider")
    _support_email_locator = (By.CSS_SELECTOR, ".support > .narrow.c > .support-email")
    _privacy_policy_locator = (By.CSS_SELECTOR, ".wide > .more-info > .privacy")
    _published_date_locator = (By.CSS_SELECTOR, ".wide > .published > p > time")

    def __init__(self, testsetup, app_name=False):
        Base.__init__(self, testsetup)
        self.wait_for_ajax_on_page_finish()
        if app_name:
            self._page_title = "%s | Mozilla Marketplace" % app_name
            self.app_name = app_name

    @property
    def is_app_available_for_purchase(self):
        return self.is_element_present(*self._purchase_locator)

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
    def app_dev_username(self):
        return self.is_element_present(*self._app_dev_username_locator)

    @property
    def weekly_downloads(self):
        return self.is_element_present(*self._weekly_downloads_locator)

    @property
    def is_image_visible(self):
        return self.is_element_visible(*self._image_locator)

    @property
    def are_section_devices_present(self):
        return self.is_element_present(*self._section_device_icon_locator)

    @property
    def is_application_description_present(self):
        return self.is_element_present(*self._application_description_locator)

    @property
    def is_image_preview_section_present(self):
        return self.is_element_present(*self._image_preview_section_locator)

    @property
    def is_support_email_present(self):
        return self.is_element_present(*self._support_email_locator)

    @property
    def is_privacy_policy_link_present(self):
        return self.is_element_present(*self._privacy_policy_locator)

    @property
    def is_published_date_present(self):
        return self.is_element_present(*self._published_date_locator)

    @property
    def is_install_button_visible(self):
        return self.is_element_visible(*self._install_locator)

    @property
    def install_purchased_button_present(self):
        return self.is_element_visible(*self._install_purchased_locator)

    @property
    def purchased_button_present(self):
        return self.is_element_visible(*self._purchase_locator)

    def click_purchase(self):
        self.selenium.find_element(*self._purchase_locator).click()
        return self.PreApproval(self.testsetup)

    def click_statistics(self):
        self.selenium.find_element(*self._statistics_link_locator).click()
        from pages.desktop.consumer_pages.statistics import Statistics
        return Statistics(self.testsetup)

    def click_submit_review(self):
        self.selenium.find_element(*self._submit_review_link_locator).click()
        from pages.desktop.consumer_pages.add_review import AddReview
        return AddReview(self.testsetup, self.app_name)

    class PreApproval(Page):
        _root_locator = (By.ID, 'pay')
        _one_time_payment_locator = (By.ID, 'payment-confirm')
        def __init__(self, testsetup):
            Page.__init__(self, testsetup)
            self._root_element = self.selenium.find_element(*self._root_locator)

        @property
        def is_visible(self):
            return self._root_element.is_displayed()

        def click_one_time_payment(self):
            self.selenium.find_element(*self._one_time_payment_locator).click()
            from pages.desktop.paypal.paypal_frame import PayPalFrame
            return PayPalFrame(self.testsetup)
