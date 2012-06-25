#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.page import Page
from restmail.restmail import RestmailInbox


class Login(Page):

    _page_title = "Mozillian Preview | Mozilla Marketplace"

    _login_locator = (By.CSS_SELECTOR, "a.browserid")

    def click_login_register(self, expect='returning'):
        """Click the 'Log in/Register' button.

        Keyword arguments:
        expect -- the expected resulting page
        'new' for user that is not currently signed in
        'returning' for users already signed in or recently verified (default)
        """
        self.selenium.find_element(*self._login_locator).click()
        from browserid.pages.webdriver.sign_in import SignIn
        return SignIn(self.selenium, self.timeout, expect=expect)

    def create_new_user(self, user):
        #saves the current url
        current_url = self.selenium.current_url

        bid_login = self.click_login_register(expect="new")

        # creates the new user in the browserID pop up
        bid_login.sign_in_new_user(user['email'], user['password'])

        # Open restmail inbox, find the email
        inbox = RestmailInbox(user['email'])
        email = inbox.find_by_index(0)

        # Load the BrowserID link from the email in the browser
        self.selenium.get(email.verify_user_link)
        from browserid.pages.webdriver.complete_registration import CompleteRegistration
        CompleteRegistration(self.selenium, self.timeout)

        # restores the current url
        self.selenium.get(current_url)
