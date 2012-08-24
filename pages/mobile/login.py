#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.mobile.base import Base
from mocks.mock_user import MockUser


class Login(Base):

    _data_body_class = "login"
    _login_locator = (By.CSS_SELECTOR, 'a.browserid')

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

    def login_with_user(self, user = "default"):
        """Logins to page using the provided user
        It doesn't wait for the page to load
        """
        if isinstance(user, MockUser):
            bid_login = self.click_login_register(expect='returning')
            bid_login.click_sign_in_returning_user()

        elif isinstance(user, str):
            bid_login = self.click_login_register(expect='new')
            credentials = self.testsetup.credentials[user]
            bid_login.sign_in(credentials['email'], credentials['password'])

        else:
            return False
