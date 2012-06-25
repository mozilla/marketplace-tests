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
    _purcasing_button_locator = (By.CSS_SELECTOR, "section.product-details > div.actions > a.button product premium purchasing")
    _preapproval_checkmark_locator = (By.CSS_SELECTOR, "section.product-details > div.actions > span.approval.checkmark")

    def __init__(self, testsetup, app_name=False):
        Base.__init__(self, testsetup)
        if app_name:
            self._page_title = "%s | Mozilla Marketplace" % app_name

    @property
    def is_app_available_for_purchase(self):
        return self.is_element_visible(*self._purchase_locator)

    @property
    def is_app_installing(self):
        self.wait_for_element_present(*self._install_purchased_locator)
        return self.is_element_visible(*self._install_purchased_locator)

    @property
    def is_app_purchasing(self):
        self.wait_for_element_present(*self._purcasing_button_locator)
        return self.is_element_visible(*self._purcasing_button_locator)

    @property
    def is_preapproval_checkmark_present(self):
        return self.is_element_present(*self._preapproval_checkmark_locator)

    @property
    def preapproval_checkmark_text(self):
        return self.selenium.find_element(*self._preapproval_checkmark_locator).text

    def click_purchase(self):
        self.selenium.find_element(*self._purchase_locator).click()
        if self.is_preapproval_checkmark_present:
            return self
        else:
            return self.PreApproval(self.testsetup)

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
