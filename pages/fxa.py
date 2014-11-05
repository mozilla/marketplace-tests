#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from fxa_test_user import FxaTestUser
from pages.desktop.consumer_pages.base import Base
from mocks.mock_user import MockUser


class FirefoxAccounts(Base):

        _page_title = 'Sign in Continue to Firefox Marketplace'

        _email_input_locator = (By.CSS_SELECTOR, '.input-row .email')
        _next_button_locator = (By.ID, 'email-button')
        _password_input_locator = (By.ID, 'password')
        _sign_in_locator = (By.ID, 'submit-btn')
        _fxa_signin_header_locator = (By.ID, 'fxa-signin-header')
        _notice_form_locator = (By.CSS_SELECTOR, '#notice-form button')

        def __init__(self, testsetup):
            Base.__init__(self, testsetup)
            self._main_window_handle = self.selenium.current_window_handle
            if self._page_title not in self.selenium.title:
                for handle in self.selenium.window_handles:
                    self.selenium.switch_to.window(handle)
                    WebDriverWait(self.selenium, self.timeout).until(lambda s: s.title)
                    if self.is_element_visible(*self._notice_form_locator):
                        self.find_element(*self._notice_form_locator).click()
                    if self._page_title in self.selenium.title:
                        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.is_element_visible(*self._email_input_locator))
                        break
            else:
                raise Exception('Popup has not loaded')

        def login_user(self, mozwebqa, user=None, email=None, password=None):
            credentials = isinstance(user, MockUser) and user or self.testsetup.credentials.get(user, FxaTestUser().create_user(mozwebqa))
            self.enter_email(credentials['email'])
            if self.is_element_visible(*self._next_button_locator):
                self.click_next()
            self.enter_password(credentials['password'])
            self.click_sign_in()

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

        def click_next(self):
            self.selenium.find_element(*self._next_button_locator).click()
