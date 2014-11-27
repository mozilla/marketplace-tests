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
        fxa = self.header.click_login()
        fxa.login_user(user)
        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.header.is_user_logged_in)

    @property
    def page_title(self):
        WebDriverWait(self.selenium, 10).until(lambda s: self.selenium.title)
        return self.selenium.title

    @property
    def header(self):
        return self.HeaderRegion(self.testsetup)

    @property
    def left_nav_menu(self):
        return self.LeftNavMenu(self.testsetup)

    class HeaderRegion(Page):

        #Not LoggedIn
        _login_locator = (By.CSS_SELECTOR, 'a.browserid:not(.register)')

        #LoggedIn
        _account_menu_locator = (By.CSS_SELECTOR, '.header-button.icon.settings')
        _logout_locator = (By.CSS_SELECTOR, '.logout')
        _my_submissions_locator = (By.CSS_SELECTOR, '.devhub-links > [href*=submissions]')

        def _hover_user_menu(self):
            # Activate user menu
            account_menu = self.selenium.find_element(*self._account_menu_locator)
            ActionChains(self.selenium).move_to_element(account_menu).perform()

        @property
        def is_user_logged_in(self):
            return self.is_element_visible(*self._account_menu_locator)

        def click_login(self):
            self.selenium.find_element(*self._login_locator).click()
            from pages.fxa import FirefoxAccounts
            return FirefoxAccounts(self.testsetup)

        def click_logout(self):
            element = self.selenium.find_element(*self.logout_locator)

            self._hover_user_menu()
            element.click()

        def click_my_submissions(self):
            element = self.selenium.find_element(*self._my_submissions_locator)
            element.click()
            from pages.desktop.developer_hub.developer_submissions import DeveloperSubmissions
            return DeveloperSubmissions(self.testsetup)

    class LeftNavMenu(Page):

        _status_link_locator = (
            By.CSS_SELECTOR,
            'section.secondary ul.refinements:nth-child(1) li:nth-child(2) a')
        _compatibility_and_payments_link_locator = (
            By.CSS_SELECTOR,
            'section.secondary ul.refinements:nth-child(1) li:nth-child(4) a')

        def click_status(self):
            self.selenium.find_element(*self._status_link_locator).click()
            from pages.desktop.developer_hub.manage_status import ManageStatus
            return ManageStatus(self.testsetup)

        def click_compatibility_and_payments(self):
            self.selenium.find_element(*self._compatibility_and_payments_link_locator).click()
            from pages.desktop.developer_hub.compatibility_and_payments import CompatibilityAndPayments
            return CompatibilityAndPayments(self.testsetup)
