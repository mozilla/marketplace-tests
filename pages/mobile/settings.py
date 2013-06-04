#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

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
    _logout_locator = (By.CSS_SELECTOR, '.button.alt.logout.only-logged-in')
    _login_locator = (By.CSS_SELECTOR, '.button.alt.persona.only-logged-out')
    _notification_locator = (By.ID, 'notification-content')

    _settings_options_locator = (By.CSS_SELECTOR, '.toggles.c li a[href="%s"]')
    _selected_option_locator = (By.CLASS_NAME, 'sel')

    def __init__(self, testsetup):
        Settings.__init__(self, testsetup)

    @property
    def email_text(self):
        return self.selenium.find_element(*self._email_locator).get_attribute("value")

    def click_on_notification(self):
        self.selenium.find_element(*self._notification_locator).click()

    def click_logout(self):
        self.scroll_to_element(*self._logout_locator)
        self.selenium.find_element(*self._logout_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.is_element_not_visible(*self._logout_locator))
        from pages.mobile.home import Home
        return Home(self.testsetup)

    def login(self, user=None):
        self.selenium.find_element(*self._login_locator).click()
        credentials = isinstance(user, MockUser) and user or self.testsetup.credentials.get(user, PersonaTestUser().create_user())

        bid_login = self.click_sign_in(expect='new')
        bid_login.sign_in(credentials['email'], credentials['password'])

        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.is_element_visible(*self._notification_locator))

    def click_sign_in(self, expect='new'):
        """Click the 'Sign in/Sign out' button.

        Keyword arguments:
        expect -- the expected resulting page
        'new' for user that is not currently signed in (default)
        'returning' for users already signed in or recently verified
        """
        self.selenium.find_element(*self._login_locator).click()
        from browserid.pages.sign_in import SignIn
        return SignIn(self.selenium, self.timeout, expect=expect)

    def click_apps(self):
        self.selenium.find_element(self._settings_options_locator[0], self._settings_options_locator[1] % ("/purchases")).click()
        WebDriverWait(self.selenium, self.timeout).until(lambda s: s.find_element(*self._selected_option_locator).text == 'My Apps')
        return self.Apps

    @property
    def is_sign_in_visible(self):
        return self.is_element_visible(*self._login_locator)

    @property
    def selected_settings_option(self):
        return self.selenium.find_element(*self._selected_option_locator).text

    class Apps(Settings):
        pass
