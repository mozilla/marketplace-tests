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
        credentials = self.testsetup.credentials[user]
        fxa.enter_email(credentials['email'])
        fxa.click_next()
        fxa.enter_password(credentials['password'])
        fxa.click_sign_in()
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
        _login_locator = (By.CSS_SELECTOR, 'a.browserid')

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

class FirefoxAccounts(Base):

        _page_title = 'Firefox Marketplace'

        _notice_form_locator = (By.CSS_SELECTOR, '#notice-form button')
        _email_input_locator = (By.CSS_SELECTOR, '.input-row .email')
        _next_button_locator = (By.ID, 'email-button')
        _password_input_locator = (By.ID, 'password')
        _sign_in_locator = (By.ID, 'submit-btn')

        def __init__(self, testsetup):
            Base.__init__(self, testsetup)
            self._main_window_handle = self.selenium.current_window_handle
            if self.selenium.title != self._page_title:
                for handle in self.selenium.window_handles:
                    self.selenium.switch_to.window(handle)
                    WebDriverWait(self.selenium, self.timeout).until(lambda s: s.title)
                    if self.is_element_visible(*self._notice_form_locator):
                        self.find_element(*self._notice_form_locator).click()
                    if self.selenium.title == self._page_title:
                        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.is_element_visible(*self._email_input_locator))
                        break
            else:
                raise Exception('Popup has not loaded')

        def enter_password(self, value):
            password = self.selenium.find_element(*self._password_input_locator)
            password.send_keys(value)

        def enter_email(self, value):
            email = self.selenium.find_element(*self._email_input_locator)
            email.send_keys(value)

        def click_sign_in(self):
            self.selenium.find_element(*self._sign_in_locator).click()
            self.selenium.switch_to.window(self._main_window_handle)
            
        def click_next(self):
            self.selenium.find_element(*self._next_button_locator).click()
