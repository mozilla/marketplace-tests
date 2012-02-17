#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.desktop.base import Base


class Login(Base):

    _page_title = 'User Login :: Apps Developer Preview'

    _logout_locator = (By.CSS_SELECTOR, 'li.account > a.user')

    def login(self, user):
        credentials = self.testsetup.credentials[user]
        from pages.desktop.browserid import BrowserID
        pop_up = BrowserID(self.selenium, self.timeout)
        pop_up.sign_in(credentials['email'], credentials['password'])
        WebDriverWait(self.selenium, 20).until(lambda s: s.find_element(*self._logout_locator))
