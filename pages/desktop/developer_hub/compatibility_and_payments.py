#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from mocks.mock_bango_payment_account import MockBangoPaymentAccount
from pages.page import Page
from pages.desktop.developer_hub.base import Base


class CompatibilityAndPayments(Base):

    _device_type_locator = (By.CSS_SELECTOR, '.free.tab.active div.wrapper a')
    _device_types_error_locator = (By.CSS_SELECTOR, '.free.tab.active > .error')
    _save_changes_locator = (By.CSS_SELECTOR, '#compat-save-button > button')

    _payment_accounts_drop_down_locator = (By.ID, 'id_form-0-accounts')
    _payment_account_action_link_locator = (By.ID, 'payment-account-action')
    _add_payment_account_button_locator = (By.CSS_SELECTOR, '.add-payment-account.button')
    _add_payment_account_header_locator = (By.CSS_SELECTOR, '#payment-account-add header h2')

    _register_payment_account_button_locator = (By.CSS_SELECTOR, '#payment-account-add button')
    _agree_to_the_terms_button_locator = (By.CSS_SELECTOR, '#show-agreement button')

    _price_drop_down_locator = (By.ID, 'id_price')
    _price_section_locator = (By.CSS_SELECTOR, 'section#regions')
    _save_payments_changes_locator = (By.CSS_SELECTOR, '#paid-regions-island .listing-footer > button')
    _changes_saved_notification_locator = (By.CSS_SELECTOR, '.notification-box.success')

    @property
    def add_payment_account_header_text(self):
        return self.selenium.find_element(*self._add_payment_account_header_locator).text

    def add_payment_account(self):
        self.selenium.find_element(*self._payment_account_action_link_locator).click()
        self.wait_for_element_visible(*self._add_payment_account_button_locator)
        self.selenium.find_element(*self._add_payment_account_button_locator).click()
        self.wait_for_element_visible(*self._add_payment_account_header_locator)
        if 'Bango' in self.add_payment_account_header_text:
            self.AddBangoAccountForm(self.testsetup).complete_form()
        else:
            self.AddReferenceAccountForm(self.testsetup).complete_form()
        self.selenium.find_element(*self._register_payment_account_button_locator).click()
        self.wait_for_element_visible(*self._agree_to_the_terms_button_locator)
        self.selenium.find_element(*self._agree_to_the_terms_button_locator).click()

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
                    lambda s: self.selenium.execute_script('return jQuery.active == 0')
                    and'loading' not in s.find_element(*self._price_section_locator).get_attribute('class').split(' '))
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

    @property
    def is_update_notification_visible(self):
        return self.is_element_visible(*self._changes_saved_notification_locator)

    class AddBangoAccountForm(Base):

        _bank_account_holder_name_input_locator = (By.ID, 'id_bankAccountPayeeName')
        _bank_account_number_input_locator = (By.ID, 'id_bankAccountNumber')
        _bank_account_code_input_locator = (By.ID, 'id_bankAccountCode')
        _address_input_locator = (By.ID, 'id_address1')
        _city_input_locator = (By.ID, 'id_addressCity')
        _state_input_locator = (By.ID, 'id_addressState')
        _zip_code_input_locator = (By.ID, 'id_addressZipCode')
        _phone_input_locator = (By.ID, 'id_addressPhone')
        _bank_name_input_locator = (By.ID, 'id_bankName')
        _bank_address_input_locator = (By.ID, 'id_bankAddress1')
        _bank_zip_code_input_locator = (By.ID, 'id_bankAddressZipCode')
        _company_name_input_locator = (By.ID, 'id_companyName')
        _vendor_name_input_locator = (By.ID, 'id_vendorName')
        _finance_email_input_locator = (By.ID, 'id_financeEmailAddress')
        _admin_email_input_locator = (By.ID, 'id_adminEmailAddress')
        _support_email_input_locator = (By.ID, 'id_supportEmailAddress')
        _account_name_input_locator = (By.ID, 'id_account_name')

        def complete_form(self, account=MockBangoPaymentAccount()):
            self.selenium.find_element(
                *self._bank_account_holder_name_input_locator).send_keys(account.bank_account_holder_name)
            self.selenium.find_element(
                *self._bank_account_number_input_locator).send_keys(account.bank_account_number)
            self.selenium.find_element(
                *self._bank_account_code_input_locator).send_keys(account.bank_account_code)
            self.selenium.find_element(
                *self._address_input_locator).send_keys(account.address)
            self.selenium.find_element(
                *self._city_input_locator).send_keys(account.city)
            self.selenium.find_element(
                *self._state_input_locator).send_keys(account.state)
            self.selenium.find_element(
                *self._zip_code_input_locator).send_keys(account.zip_code)
            self.selenium.find_element(
                *self._phone_input_locator).send_keys(account.phone)
            self.selenium.find_element(
                *self._bank_name_input_locator).send_keys(account.bank_name)
            self.selenium.find_element(
                *self._bank_address_input_locator).send_keys(account.bank_address)
            self.selenium.find_element(
                *self._bank_zip_code_input_locator).send_keys(account.bank_zip_code)
            self.selenium.find_element(
                *self._company_name_input_locator).send_keys(account.company_name)
            self.selenium.find_element(
                *self._vendor_name_input_locator).send_keys(account.vendor_name)
            self.selenium.find_element(
                *self._finance_email_input_locator).send_keys(account.finance_email)
            self.selenium.find_element(
                *self._admin_email_input_locator).send_keys(account.admin_email)
            self.selenium.find_element(
                *self._support_email_input_locator).send_keys(account.support_email)
            self.selenium.find_element(
                *self._account_name_input_locator).send_keys(account.account_name)

    class AddReferenceAccountForm(Base):

        _account_name_input_locator = (By.ID, 'id_account_name')
        _name_input_locator = (By.ID, 'id_name')
        _email_input_locator = (By.ID, 'id_email')

        def complete_form(self):
            self.selenium.find_element(
                *self._account_name_input_locator).send_keys('Test account name')
            self.selenium.find_element(
                *self._name_input_locator).send_keys('Test name')
            self.selenium.find_element(
                *self._email_input_locator).send_keys('test_email@mozilla.com')


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
        checked checkbox returns True
        unchecked checkbox returns False"""
        return self._root_element.find_element(*self._check_box_locator).is_selected()

    def change_state(self):
        """change the state of the checkbox:
            checked => unchecked
            unchecked => checked"""
        self._root_element.find_element(*self._check_box_locator).find_element(By.XPATH, "..").click()
