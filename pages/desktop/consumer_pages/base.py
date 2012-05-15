#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.page import Page
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class Base(Page):

    def login(self, user="default"):
        from pages.desktop.login import Login
        login_page = Login(self.testsetup)
        login_page.click_login()

        credentials = self.testsetup.credentials[user]
        from browserid import BrowserID
        pop_up = BrowserID(self.selenium, self.timeout)
        pop_up.sign_in(credentials['email'], credentials['password'])
        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.footer.is_user_logged_in)

    @property
    def footer(self):
        return self.FooterRegion(self.testsetup)

    class FooterRegion(Page):

        _account_controller_locator = (By.CSS_SELECTOR, "#site-footer > a:nth-child(1)")
        _logout_locator = (By.CSS_SELECTOR, "#site-footer > a:nth-child(2)")

        @property
        def is_user_logged_in(self):
            return self.is_element_visible(*self._account_controller_locator)

        def click_logout(self):
            self.selenium.find_element(*self._logout_locator).click()

