#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.desktop.consumer_pages.base import Base
from selenium.webdriver.support.ui import WebDriverWait


class AccountSettings(Base):
    """
    Account settings base page
    Contains the common objects in the account setting area
    """
    _payment_locator = (By.CSS_SELECTOR, '.sub-nav > li:nth-child(2) > a')
    _header_title_locator = (By.CSS_SELECTOR, 'header.c > h1')
    _payment_page_locator = (By.ID, 'purchases')

    def click_payment_menu(self):
        self.selenium.find_element(*self._payment_locator).click()
        self.wait_for_page_loaded()
        return Payments(self.testsetup)

    @property
    def header_title(self):
        return self.selenium.find_element(*self._header_title_locator).text

    def wait_for_page_loaded(self):
        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.is_element_present(*self._payment_page_locator))

class BasicInfo(AccountSettings):
    """
    User Account Settings page
    https://marketplace-dev.allizom.org/en-US/settings/
    """

    _page_title = "Account Settings | Mozilla Marketplace"


class Payments(AccountSettings):
    """
    Payment Settings page
    https://marketplace-dev.allizom.org/en-US/settings/payment
    """

    _page_title = "Payment Settings | Mozilla Marketplace"

    _set_up_pre_approval_locator = (By.CSS_SELECTOR, '#preapproval > footer > button')
    _pre_approval_enabled_locator = (By.CSS_SELECTOR, '#preapproval .enabled')
    _remove_pre_approval_locator = (By.CSS_SELECTOR, '#preapproval > footer > button.delete')
    _preapproval_success_message_locator = (By.CSS_SELECTOR, 'section.notification-box.full > div.success')

    def go_to_payment(self):
        self.selenium.get('%s/settings/payment/' % self.base_url)

    @property
    def is_success_message_visible(self):
        return self.is_element_visible(*self._preapproval_success_message_locator)

    def click_set_up_pre_approval(self):
        self.selenium.find_element(*self._set_up_pre_approval_locator).click()
        from pages.desktop.paypal.paypal_sandbox import PayPalSandbox
        return PayPalSandbox(self.testsetup)

    @property
    def is_pre_approval_enabled(self):
        return self.is_element_visible(*self._pre_approval_enabled_locator)

    @property
    def pre_approval_enabled(self):
        return self.selenium.find_element(*self._pre_approval_enabled_locator).text

    def click_remove_pre_approval(self):
        self.selenium.find_element(*self._remove_pre_approval_locator).click()

    @property
    def is_remove_pre_approval_button_visible(self):
        return self.is_element_visible(*self._remove_pre_approval_locator)
