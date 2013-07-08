#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.page import Page
from pages.desktop.developer_hub.base import Base


class CompatibilityAndPayments(Base):

    _device_type_locator = (By.CSS_SELECTOR, '.free.tab.active div.wrapper a')
    _device_types_error_locator = (By.CSS_SELECTOR, '.free.tab.active > .error')
    _save_changes_locator = (By.CSS_SELECTOR, '#compat-save-button > button')

    _price_drop_down_locator = (By.ID, 'id_price')
    _payment_accounts_drop_down_locator = (By.ID, 'id_accounts')
    _price_section_locator = (By.CSS_SELECTOR, 'section#regions')
    _save_payments_changes_locator = (By.CSS_SELECTOR, '#paid-regions-island .listing-footer > button')
    _changes_saved_notification_locator = (By.CSS_SELECTOR, '.notification-box.success > h2')

    def clear_device_types(self):
        """Sets all device type checkboxes to unchecked"""
        for device in self.selenium.find_elements(*self._device_type_locator):
            device_type_checkbox = CheckBox(self.testsetup, device)
            if device_type_checkbox.state is True:
                device_type_checkbox.change_state()

    def select_device_type(self, name, state):
        """Set the value of a single device type checkbox.

        Arguments:
        name -- the name of the checkbox to set
        state -- the state to leave the checkbox in

        """
        for device in self.selenium.find_elements(*self._device_type_locator):
            device_type_checkbox = CheckBox(self.testsetup, device)
            if device_type_checkbox.name == name:
                if device_type_checkbox.state != state:
                    device_type_checkbox.change_state()

    def select_price(self, price):
        """Select the Price Tier for app.

        Arguments:
        price -- localized string of price
        """
        price_el = self.selenium.find_element(*self._price_drop_down_locator)
        for option in price_el.find_elements(By.CSS_SELECTOR, 'option'):
            if option.text == price:
                option.click()
                WebDriverWait(self.selenium, self.timeout).until(
                    lambda s: 'loading' not in s.find_element(*self._price_section_locator).get_attribute('class').split(' '))
                break

    def select_payment_account(self):
        """Select a payment account.
        """
        accounts_el = self.selenium.find_element(*self._payment_accounts_drop_down_locator)
        accounts = accounts_el.find_elements(By.CSS_SELECTOR, 'option')
        if len(accounts) == 1:
            raise Exception('Payment accounts have not been setup.')

        for account in accounts:
            if account.get_attribute('value') != '':
                account.click()
                break

    @property
    def app_price(self):
        """Return the price of the app."""
        price_el = self.selenium.find_element(*self._price_drop_down_locator)
        for option in price_el.find_elements(By.CSS_SELECTOR, 'option'):
            if option.get_attribute('selected') is not None:
                return option.text

        return None

    @property
    def device_types_error_message(self):
        """Return the error message displayed for the device types."""
        return self.selenium.find_element(*self._device_types_error_locator).text

    def click_save_changes(self):
        self.selenium.find_element(*self._save_changes_locator).click()

    def click_payments_save_changes(self):
        self.selenium.find_element(*self._save_payments_changes_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: s.find_element(*self._changes_saved_notification_locator).is_displayed())


class CheckBox(Page):

    _check_box_locator = (By.CSS_SELECTOR, '.listing-footer > input')
    _name_locator = (By.CSS_SELECTOR, '.wrapper h3')

    def __init__(self, testsetup, root_element):
        Page.__init__(self, testsetup)
        self._root_element = root_element

    @property
    def name(self):
        """Returns the name (label) of the checkbox."""
        return self._root_element.find_element(*self._name_locator).text

    @property
    def state(self):
        """Returns the state of the checkbox:
        checked checkox returns True
        unchecked checbox returns False"""
        return self._root_element.find_element(*self._check_box_locator).is_selected()

    def change_state(self):
        """changest the state of the checkbox:
            checked => unchecked
            unchecked => checked"""
        self._root_element.find_element(*self._check_box_locator).find_element(By.XPATH, "..").click()
