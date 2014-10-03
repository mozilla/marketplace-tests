#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from mocks.mock_user import MockUser

from pages.mobile.base import Base


class AccountSettings(Base):

    _page_title = "Account Settings | Firefox Marketplace"

    _email_locator = (By.ID, 'email')
    _logout_locator = (By.CSS_SELECTOR, '.button.logout.only-logged-in')
    _login_locator = (By.CSS_SELECTOR, '.button.persona.only-logged-out')

    _settings_options_locator = (By.CSS_SELECTOR, '.nav-settings li a[href="%s"]')
    _no_apps_locator = (By.CSS_SELECTOR, '.no-results')

    def __init__(self, testsetup):
        Base.__init__(self, testsetup)

    @property
    def email_text(self):
        self.wait_for_element_visible(*self._email_locator)
        return self.selenium.find_element(*self._email_locator).get_attribute("value")

    def wait_for_user_email_visible(self):
        self.wait_for_element_visible(*self._email_locator)

    def click_logout(self):
        self.scroll_to_element(*self._logout_locator)
        self.selenium.find_element(*self._logout_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.is_element_not_visible(*self._logout_locator))
        from pages.mobile.home import Home
        return Home(self.testsetup)

    def login(self, user=None):
        fxa = self.click_sign_in()
        fxa.login_user(user)

    def click_sign_in(self, expect='new'):
        self.selenium.find_element(*self._login_locator).click()
        from pages.fxa import FirefoxAccounts
        return FirefoxAccounts(self.testsetup)

    def click_apps(self):
        self.selenium.find_element(self._settings_options_locator[0], self._settings_options_locator[1] % ("/purchases")).click()
        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.is_element_visible(*self._no_apps_locator))

    @property
    def is_sign_in_visible(self):
        return self.is_element_visible(*self._login_locator)
