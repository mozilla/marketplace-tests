#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.mobile.base import Base


class Settings(Base):

    pass


class Account(Settings):
    _page_title = "Account Settings | Firefox Marketplace"

    _email_locator = (By.ID, 'email')
    _logout_locator = (By.CSS_SELECTOR, 'a.fatbutton.logout')
    _login_locator = (By.CSS_SELECTOR, 'a.fatbutton.browserid')

    _settings_options_locator = (By.CSS_SELECTOR, '.toggles.c li a[href="%s"]')
    _selected_option_locator = (By.CLASS_NAME, 'sel')

    def __init__(self, testsetup):
        Settings.__init__(self, testsetup)

    @property
    def email_text(self):
        return self.selenium.find_element(*self._email_locator).get_attribute("value")

    def click_logout(self):
        self.scroll_to_element(*self._logout_locator)
        self.selenium.find_element(*self._logout_locator).click()
        from pages.mobile.home import Home
        return Home(self.testsetup)

    def login(self):
        self.scroll_to_element(*self._login_locator)
        self.selenium.find_element(*self._login_locator).click()
        self.login_with_user_from_other_pages(user="default")
        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.is_element_present(*self._logout_locator))

    def click_apps(self):
        self.selenium.find_element(self._settings_options_locator[0], self._settings_options_locator[1] % ("/purchases/")).click()
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
