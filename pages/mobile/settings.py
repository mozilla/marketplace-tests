#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from persona_test_user import PersonaTestUser
from mocks.mock_user import MockUser

from pages.mobile.base import Base


class Settings(Base):

    pass


class Account(Settings):

    _page_title = "Account Settings | Firefox Marketplace"

    _email_locator = (By.ID, 'email')
    _logout_locator = (By.CSS_SELECTOR, '.button.logout.only-logged-in')
    _login_locator = (By.CSS_SELECTOR, '.button.persona.only-logged-out')

    _settings_options_locator = (By.CSS_SELECTOR, '.nav-settings li a[href="%s"]')
    _no_apps_locator = (By.CSS_SELECTOR, '.no-results')

    def __init__(self, testsetup):
        Settings.__init__(self, testsetup)

    @property
    def email_text(self):
        self.wait_for_element_visible(*self._email_locator)
        return self.selenium.find_element(*self._email_locator).get_attribute("value")

    def click_logout(self):
        self.scroll_to_element(*self._logout_locator)
        self.selenium.find_element(*self._logout_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.is_element_not_visible(*self._logout_locator))
        from pages.mobile.home import Home
        return Home(self.testsetup)

    def login(self, user=None):

        credentials = isinstance(user, MockUser) and user or self.testsetup.credentials.get(user, PersonaTestUser().create_user())

        fxa = self.click_sign_in()
        fxa.enter_email(credentials['email'])
        fxa.enter_password(credentials['password'])
        fxa.click_sign_in()

    def wait_for_user_email_visible(self):
        self.wait_for_element_visible(*self._email_locator)

    def click_sign_in(self, expect='new'):
        self.selenium.find_element(*self._login_locator).click()
        # wait a bit for FxA window to load
        time.sleep(8)
        return FirefoxAccounts(self.testsetup)

    def click_apps(self):
        self.selenium.find_element(self._settings_options_locator[0], self._settings_options_locator[1] % ("/purchases")).click()
        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.is_element_visible(*self._no_apps_locator))
        return self.Apps

    @property
    def is_sign_in_visible(self):
        return self.is_element_visible(*self._login_locator)

    class Apps(Settings):
        pass


class FirefoxAccounts(Base):

        _page_title = 'Sign in Continue to Firefox Marketplace DEV'

        _email_input_locator = (By.CSS_SELECTOR, '.email')
        _password_input_locator = (By.CSS_SELECTOR, '#password')
        _sign_in_locator = (By.ID, 'submit-btn')
        _fxa_signin_header_locator = (By.ID, 'fxa-signin-header')

        def __init__(self, testsetup):
            Base.__init__(self, testsetup)
            self._main_window_handle = self.selenium.current_window_handle
            if self.selenium.title != self._page_title:
                for handle in self.selenium.window_handles:
                    self.selenium.switch_to.window(handle)
                    WebDriverWait(self.selenium, self.timeout).until(lambda s: s.title)
                    if self.selenium.title == self._page_title:
                        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.is_element_visible(*self._fxa_signin_header_locator))
                        break
            else:
                raise Exception('Popup has not loaded')

        def enter_password(self, value):
            password = self.selenium.find_element(*self._password_input_locator)
            password.clear()
            password.send_keys(value)

        def enter_email(self, value):
            email = self.selenium.find_element(*self._email_input_locator)
            email.clear()
            email.send_keys(value)

        def click_sign_in(self):
            self.selenium.find_element(*self._sign_in_locator).click()
            self.selenium.switch_to.window(self._main_window_handle)
