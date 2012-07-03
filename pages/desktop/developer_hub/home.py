#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

from pages.page import Page


class Home(Page):

    _page_title = "Developers | Mozilla Marketplace"

    def go_to_developers_homepage(self):
        self.selenium.get("%s/developers/" % self.base_url)
        self.maximize_window()

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
        _login_locator = (By.CSS_SELECTOR, "div.wrapper > nav > a.browserid")

        #LoggedIn
        _my_apps_locator = (By.CSS_SELECTOR, "div.wrapper > nav > a:nth-child(2)")
        _logout_locator = (By.CSS_SELECTOR, "div.wrapper > nav > a:nth-child(4)")

        #app nav
        _submit_app_locator = (By.CSS_SELECTOR, "div.wrapper > nav > a:nth-child(1)")

        @property
        def is_user_logged_in(self):
            return self.is_element_visible(*self._logout_locator)

        def click_login(self):
            self.selenium.find_element(*self._login_locator).click()

        def click_logout(self):
            self.selenium.find_element(*self._logout_locator).click()

        def click_my_apps(self):
            self.selenium.find_element(*self._my_apps_locator).click()
            from pages.desktop.developer_hub.developer_submissions import DeveloperSubmissions
            dev_submissions = DeveloperSubmissions(self.testsetup)
            WebDriverWait(self.selenium, self.timeout).until(lambda s: dev_submissions.is_the_current_page)
            return dev_submissions

        def click_submit_app(self):
            self.selenium.find_element(*self._submit_app_locator).click()
            from pages.desktop.developer_hub.submit_app import DeveloperAgreement
            return DeveloperAgreement(self.testsetup)
