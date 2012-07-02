#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.page import Page
from mocks.mock_user import MockUser
from restmail.restmail import RestmailInbox


class Base(Page):

    _loading_balloon_locator = (By.CSS_SELECTOR, '#site-header > div.loading.balloon.active')

    @property
    def page_title(self):
        WebDriverWait(self.selenium, 10).until(lambda s: self.selenium.title)
        return self.selenium.title

    @property
    def breadcrumbs(self):
        from pages.desktop.regions.breadcrumbs import Breadcrumbs
        return Breadcrumbs(self.testsetup).breadcrumbs

    def wait_for_ajax_on_page_finish(self):
        WebDriverWait(self.selenium, self.timeout).until(lambda s: not self.is_element_present(*self._loading_balloon_locator))

    def wait_for_ajax(self):
        WebDriverWait(self.selenium, 10).until(lambda s: self.selenium.execute_script('return jQuery.active == 0'))

    def login(self, user = "default"):
        from pages.desktop.login import Login
        login_page = Login(self.testsetup)

        if isinstance(user, MockUser):
            bid_login = login_page.click_login_register(expect='returning')
            bid_login.click_sign_in_returning_user()

        elif isinstance(user, str):
            bid_login = login_page.click_login_register(expect='new')
            credentials = self.testsetup.credentials[user]
            bid_login.sign_in(credentials['email'], credentials['password'])

        else:
            return False

        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.footer.is_user_logged_in)

    def create_new_user(self, user):
        #saves the current url
        current_url = self.selenium.current_url

        from pages.desktop.login import Login
        login_page = Login(self.testsetup)
        bid_login = login_page.click_login_register(expect="new")

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

    @property
    def footer(self):
        return self.FooterRegion(self.testsetup)

    @property
    def header(self):
        return self.HeaderRegion(self.testsetup)

    class HeaderRegion(Page):

        _search_locator = (By.ID, "search-q")
        _search_arrow_locator = (By.ID, "search-go")
        _suggestion_list_title_locator = (By.CSS_SELECTOR, '#site-search-suggestions .wrap > p > a > span')
        _search_suggestions_locator = (By.CSS_SELECTOR, "#site-search-suggestions .wrap")
        _search_suggestions_list_locator = (By.CSS_SELECTOR, '#site-search-suggestions .wrap ul >li')

        def search(self, search_term, click_arrow = True):
            """
            Searches for an app using the available search field
            :Args:
             - search_term - string value of the search field
             - click_arrow - bool value that determines if the search button will be clicked or
                             should the submit method be used

            :Usage:
             - search(search_term="text", click_arrow = False)
            """
            search_field = self.selenium.find_element(*self._search_locator)
            search_field.send_keys(search_term)
            if click_arrow:
                self.selenium.find_element(*self._search_arrow_locator).click()
            else:
                search_field.submit()
            from pages.desktop.consumer_pages.search import Search
            return Search(self.testsetup, search_term)

        def type_search_term_in_search_field(self, search_term):
            search_field = self.selenium.find_element(*self._search_locator)
            search_field.send_keys(search_term)
            WebDriverWait(self.selenium, self.timeout).until(lambda s: self.is_element_visible(*self._search_suggestions_locator))

        @property
        def search_suggestions(self):
            return [self.SearchSuggestion(self.testsetup, web_element)
                for web_element in self.selenium.find_elements(*self._search_suggestions_list_locator)]

        @property
        def is_search_suggestion_list_visible(self):
            return self.is_element_visible(*self._search_suggestions_locator)

        @property
        def search_suggestion_title(self):
            return self.selenium.find_element(*self._suggestion_list_title_locator).text

        class SearchSuggestion(Page):

            _app_name_locator = (By.CSS_SELECTOR, 'a > span')

            def __init__(self, testsetup, element):
                Page.__init__(self, testsetup)
                self._root_element = element

            @property
            def app_name(self):
                return self._root_element.find_element(*self._app_name_locator).text

            @property
            def is_app_icon_displayed(self):
                image = self._root_element.find_element(*self._app_name_locator).get_attribute('style')
                return self._root_element.find_element(*self._app_name_locator).is_displayed() and ("background-image" in image)

    class FooterRegion(Page):

        _account_controller_locator = (By.CSS_SELECTOR, "#site-footer > div.account.authenticated > a:nth-child(1)")
        _logout_locator = (By.CSS_SELECTOR, "#site-footer > div.account.authenticated > a.logout")

        _account_history_locator = (By.CSS_SELECTOR, "#site-footer > nav.footer-links > a:nth-child(2)")
        _account_settings_locator = (By.CSS_SELECTOR, "#site-footer > nav.footer-links > a:nth-child(3)")

        @property
        def is_user_logged_in(self):
            return self.is_element_visible(*self._account_controller_locator)

        def click_logout(self):
            self.selenium.find_element(*self._logout_locator).click()

        def click_account_settings(self):
            self.selenium.find_element(*self._account_settings_locator).click()
            from pages.desktop.consumer_pages.account_settings import BasicInfo
            return BasicInfo(self.testsetup)

        def click_account_history(self):
            self.selenium.find_element(*self._account_history_locator).click()
            from pages.desktop.consumer_pages.account_history import AccountHistory
            return AccountHistory(self.testsetup)
