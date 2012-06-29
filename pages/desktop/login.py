#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.page import Page


class Login(Page):

    _page_title = "Mozillian Preview | Mozilla Marketplace"

    _login_locator = (By.CSS_SELECTOR, "a.browserid")

    def click_login_register(self, expect='new'):
        """Click the 'Log in/Register' button.

        Keyword arguments:
        expect -- the expected resulting page
        'new' for user that is not currently signed in (default)
        'returning' for users already signed in or recently verified
        """
        self.selenium.find_element(*self._login_locator).click()
        from browserid.pages.webdriver.sign_in import SignIn
        return SignIn(self.selenium, self.timeout, expect=expect)
