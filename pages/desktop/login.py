#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.page import Page
from selenium.webdriver.common.by import By


class Login(Page):

    _page_title = "Mozillian Preview | Mozilla Marketplace"

    _login_locator = (By.CSS_SELECTOR, "a.browserid")

    def click_login(self):
        self.selenium.find_element(*self._login_locator).click()
