#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.mobile.base import Base


class Settings(Base):

    pass


class Account(Settings):
    _page_title = "Account Settings | Firefox Marketplace"
    _data_body_class = "settings"

    _email_locator = (By.ID, 'email')
    _logout_locator = (By.CSS_SELECTOR, '.extras > .post.logout')

    def __init__(self, testsetup):
        Settings.__init__(self, testsetup)
        self.wait_for_page_to_load()

    @property
    def email_text(self):
        return self.selenium.find_element(*self._email_locator).get_attribute("value")

    def click_logout(self):
        self.selenium.find_element(*self._logout_locator).click()
        from pages.mobile.home import Home
        return Home(self.testsetup)
