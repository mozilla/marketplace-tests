# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.mobile.base import Base


class Settings(Base):

    _page_title = "Account Settings | Firefox Marketplace"

    _email_locator = (By.CSS_SELECTOR, '.settings-email.account-field > p')

    @property
    def email_text(self):
        self.wait_for_element_visible(*self._email_locator)
        return self.selenium.find_element(*self._email_locator).text

    def wait_for_user_email_visible(self):
        self.wait_for_element_visible(*self._email_locator)

    def click_sign_in(self):
        self.wait_for_element_visible(*self._sign_in_locator)
        self.selenium.find_element(*self._sign_in_locator).click()
