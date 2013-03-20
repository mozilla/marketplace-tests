#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

from pages.page import Page


class Base(Page):

    def login(self, user="default"):

        self.header.click_login()

        credentials = self.testsetup.credentials[user]
        from browserid import BrowserID
        pop_up = BrowserID(self.selenium, self.timeout)
        pop_up.sign_in(credentials['email'], credentials['password'])
        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.header.is_user_logged_in)

    @property
    def header(self):
        return self.HeaderRegion(self.testsetup)

    class HeaderRegion(Page):

        #Not LoggedIn
        _login_locator = (By.CSS_SELECTOR, 'a.browserid')

        #LoggedIn
        _account_menu_locator = (By.CSS_SELECTOR, '.header-button.icon.settings')
        _logout_locator = (By.CSS_SELECTOR, '.logout')
        _my_submissions_locator = (By.CSS_SELECTOR, '.account-links > ul > li:nth-of-type(2) > a')

        def _hover_user_menu(self):
            # Activate user menu
            account_menu = self.selenium.find_element(*self._account_menu_locator)
            ActionChains(self.selenium).move_to_element(account_menu).perform()

        @property
        def is_user_logged_in(self):
            return self.is_element_visible(*self._account_menu_locator)

        def click_login(self):
            self.selenium.find_element(*self._login_locator).click()

        def click_logout(self):
            element = self.selenium.find_element(*self.logout_locator)

            self._hover_user_menu()
            element.click()

        def click_my_submissions(self):
            element = self.selenium.find_element(*self._my_submissions_locator)

            self._hover_user_menu()
            element.click()
            from pages.desktop.developer_hub.developer_submissions import DeveloperSubmissions
            dev_submissions = DeveloperSubmissions(self.testsetup)
            WebDriverWait(self.selenium, self.timeout).until(lambda s: dev_submissions.is_the_current_page)
            return dev_submissions
