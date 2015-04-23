#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.mobile.base import Base


class Settings(Base):

    _page_title = "Account Settings | Firefox Marketplace"

    _email_locator = (By.CSS_SELECTOR, '.settings-email.account-field > p')
    _sign_out_locator = (By.CSS_SELECTOR, '.button.action.logout')
    _sign_in_locator = (By.CSS_SELECTOR, '.account-settings-save a:not(.register)')

    @property
    def email_text(self):
        self.wait_for_element_visible(*self._email_locator)
        return self.selenium.find_element(*self._email_locator).text

    def wait_for_user_email_visible(self):
        self.wait_for_element_visible(*self._email_locator)

    def click_sign_out(self):
        sign_out_button = self.selenium.find_element(*self._sign_out_locator)
        self.scroll_to_element(sign_out_button)
        sign_out_button.click()
        sign_in_button = self.selenium.find_element(*self._sign_in_locator)
        WebDriverWait(self.selenium, self.timeout).until(lambda s: sign_in_button.is_displayed())
        from pages.mobile.home import Home
        return Home(self.testsetup)

    def click_sign_in(self):
        self.wait_for_element_visible(*self._sign_in_locator)
        self.selenium.find_element(*self._sign_in_locator).click()

    @property
    def is_sign_in_visible(self):
        return self.is_element_visible(*self._sign_in_locator)
