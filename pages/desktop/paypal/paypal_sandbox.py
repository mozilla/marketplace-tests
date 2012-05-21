#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

from pages.page import Page


class PayPalSandbox(Page):
    """
    Handles the login for PayPal Sandbox page.
    https://www.sandbox.paypal.com
    """
    _page_title = "Welcome - PayPal"

    _login_link_locator = (By.CSS_SELECTOR, '.layout1 > p > strong > a')
    _login_link_tab_locator = (By.ID, 'loadLogin')
    _progress_meter_locator = (By.CSS_SELECTOR, '#panelMask .accessAid')
    _email_locator = (By.ID, 'login_email')
    _password_locator = (By.ID, 'login_password')
    _login_locator = (By.CSS_SELECTOR, '.buttons #submitLogin')
    _approve_button_locator = (By.ID, 'submit.x')

    def click_login_link(self):
        self.selenium.find_element(*self._login_link_locator).click()
        from pages.desktop.paypal.paypal import PayPal
        return PayPal(self.testsetup)

    def click_login_tab(self):
        click_element = self.selenium.find_element(*self._login_link_tab_locator)
        ActionChains(self.selenium).\
            move_to_element(click_element).\
            click().\
            perform()
        WebDriverWait(self.selenium, 10).until(lambda s: not self.is_element_visible(*self._progress_meter_locator))

    def login_paypal_sandbox(self, user="sandbox"):
        credentials = self.testsetup.credentials[user]
        self.selenium.find_element(*self._email_locator).send_keys(credentials['email'])
        self.selenium.find_element(*self._password_locator).send_keys(credentials['password'])
        self.selenium.find_element(*self._login_locator).click()
        WebDriverWait(self.selenium, 10).until(lambda s: not self.is_element_visible(*self._progress_meter_locator))

    @property
    def is_user_logged_in(self):
        return self.is_element_present(*self._approve_button_locator)

    def click_approve_button(self):
        self.selenium.find_element(*self._approve_button_locator).click()
        WebDriverWait(self.selenium, 10).until(lambda s: not self.is_element_visible(*self._progress_meter_locator))
