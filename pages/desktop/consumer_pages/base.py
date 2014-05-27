#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.page import Page
from persona_test_user import PersonaTestUser
from mocks.mock_user import MockUser


class Base(Page):

    _login_locator = (By.CSS_SELECTOR, '.header-button.persona')
    _load_home_page_balloon_locator = (By.CSS_SELECTOR, '.throbber')
    _load_page_details_baloon_locator = (By.CSS_SELECTOR, '.spinner.padded.alt')
    _notification_locator = (By.ID, 'notification')
    _notification_content_locator = (By.ID, 'notification-content')

    @property
    def page_title(self):
        WebDriverWait(self.selenium, 10).until(lambda s: self.selenium.title)
        return self.selenium.title

    def wait_for_page_to_load(self):
        self.wait_for_element_not_visible(*self._load_home_page_balloon_locator) \
                            and self.wait_for_element_not_visible(*self._load_page_details_baloon_locator)

    def scroll_to_element(self, *locator):
        """Scroll to element"""
        el = self.selenium.find_element(*locator)
        self.selenium.execute_script("window.scrollTo(0, %s)" % (el.location['y'] + el.size['height']))

    def login(self, user=None):
        credentials = isinstance(user, MockUser) and user or self.testsetup.credentials.get(user, PersonaTestUser().create_user())

        bid_login = self.click_login_register(expect='new')
        bid_login.sign_in(credentials['email'], credentials['password'])

        self.wait_notification_box_visible()
        self.wait_notification_box_not_visible()

    def click_login_register(self, expect='new'):
        """Click the 'Log in/Register' button.

        Keyword arguments:
        expect -- the expected resulting page
        'new' for user that is not currently signed in (default)
        'returning' for users already signed in or recently verified
        """
        self.selenium.find_element(*self._login_locator).click()
        from browserid.pages.sign_in import SignIn
        return SignIn(self.selenium, self.timeout, expect=expect)

    @property
    def notification_visible(self):
        return self.is_element_visible(*self._notification_locator)

    @property
    def notification_message(self):
        return self.selenium.find_element(*self._notification_content_locator).text

    def wait_notification_box_visible(self):
        self.wait_for_element_visible(*self._notification_locator)

    def wait_notification_box_not_visible(self):
        self.wait_for_element_not_visible(*self._notification_locator)

    @property
    def header(self):
        return self.HeaderRegion(self.testsetup)

    class HeaderRegion(Page):

        _search_locator = (By.ID, 'search-q')
        _suggestion_list_title_locator = (By.CSS_SELECTOR, '#site-search-suggestions .wrap > p > a > span')
        _search_suggestions_locator = (By.CSS_SELECTOR, '#site-search-suggestions')
        _search_suggestions_list_locator = (By.CSS_SELECTOR, '#site-search-suggestions > ul > li')
        _site_logo_locator = (By.CSS_SELECTOR, '.site > a')
        _account_settings_locator = (By.CSS_SELECTOR, '.header-button.settings')
        _edit_user_settings_locator = (By.CSS_SELECTOR, '.account-links.only-logged-in > ul > li > a')
        _sign_out_locator = (By.CSS_SELECTOR, '.logout')
        _sign_in_locator = (By.CSS_SELECTOR, '.header-button.persona')

        @property
        def is_user_logged_in(self):
            return self.is_element_visible(*self._account_settings_locator)

        def hover_over_settings_menu(self):
            hover_element = self.selenium.find_element(*self._account_settings_locator)
            ActionChains(self.selenium).\
                move_to_element(hover_element).\
                perform()

        def click_sign_out(self):
            self.hover_over_settings_menu()
            self.selenium.find_element(*self._sign_out_locator).click()
            self.wait_for_element_visible(*self._sign_in_locator)

        def click_edit_account_settings(self):
            self.hover_over_settings_menu()
            self.selenium.find_element(*self._edit_user_settings_locator).click()
            from pages.desktop.consumer_pages.account_settings import BasicInfo
            return BasicInfo(self.testsetup)

        def search(self, search_term):
            """
            Searches for an app using the available search field
            :Args:

             - search_term - string value of the search field
            """
            search_field = self.selenium.find_element(*self._search_locator)
            search_field.send_keys(search_term)
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

        @property
        def search_field_placeholder(self):
            return self.selenium.find_element(*self._search_locator).get_attribute('placeholder')

        @property
        def is_logo_visible(self):
            return self.is_element_visible(*self._site_logo_locator)

        @property
        def is_search_visible(self):
            return self.is_element_visible(*self._search_locator)

        @property
        def is_sign_in_visible(self):
            return self.is_element_visible(*self._sign_in_locator)

        class SearchSuggestion(Page):

            _app_name_locator = (By.CSS_SELECTOR, 'a > span')

            def __init__(self, testsetup, element):
                Page.__init__(self, testsetup)
                self._root_element = element

            @property
            def app_name(self):
                return self._root_element.find_element(*self._app_name_locator).text

        @property
        def menu(self):
            return self.Menu(self.testsetup)
