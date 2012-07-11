#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.page import Page


class PayPalPermissionsSandbox(Page):
    """
    Handles the login for PayPal Permissions Sandbox page.
    https://www.sandbox.paypal.com
    """

    _email_locator = (By.ID, 'login_email')
    _password_locator = (By.ID, 'login_password')
    _login_button_locator = (By.ID, 'login.x')

    _grant_permission_locator = (By.CSS_SELECTOR, 'p.buttons > input.primary.button')

    def login_paypal_sandbox(self, user="sandbox"):
        credentials = self.testsetup.credentials[user]
        self.type_in_element(self._email_locator, credentials['email'])
        self.type_in_element(self._password_locator, credentials['password'])
        self.selenium.find_element(*self._login_button_locator).click()

    def click_grant_permission(self):
        self.selenium.find_element(*self._grant_permission_locator).click()

        from pages.desktop.developer_hub.submit_app import ConfirmContactInformation
        return ConfirmContactInformation(self.testsetup, True)
