#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.page import Page


class PayPal(Page):
    """
    PayPal developer page.
    https://developer.paypal.com/
    """

    _page_title = "PayPal Sandbox - Log In"

    _email_locator = (By.ID, 'login_email')
    _password_locator = (By.ID, 'login_password')
    _login_locator = (By.CSS_SELECTOR, 'input.formBtnOrange')
    _logout_locator = (By.CSS_SELECTOR, '#nav-global > li:nth-child(3)')

    @property
    def is_user_logged_in(self):
        return self.is_element_visible(*self._logout_locator)

    def go_to_page(self):
        self.selenium.get('https://developer.paypal.com/')

    def login_paypal(self, user="paypal"):
        credentials = self.testsetup.credentials[user]
        self.selenium.find_element(*self._email_locator).send_keys(credentials['email'])
        self.selenium.find_element(*self._password_locator).send_keys(credentials['password'])
        self.selenium.find_element(*self._login_locator).click()
