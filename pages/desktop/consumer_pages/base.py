#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from pages.page import Page
from mocks.mock_user import MockUser
from restmail.restmail import RestmailInbox


class Base(Page):

    _loading_balloon_locator = (By.CSS_SELECTOR, '.loading-fragment.overlay.active')
    _login_locator = (By.CSS_SELECTOR, 'a.browserid')

    @property
    def page_title(self):
        WebDriverWait(self.selenium, 10).until(lambda s: self.selenium.title)
        return self.selenium.title

    def wait_for_ajax_on_page_finish(self):
        WebDriverWait(self.selenium, self.timeout).until(lambda s: not self.is_element_present(*self._loading_balloon_locator)
                                                         and self.selenium.execute_script('return jQuery.active == 0'))

    def login(self, user='default'):

        if isinstance(user, MockUser):
            bid_login = self.click_login_register(expect='returning')
            bid_login.click_sign_in_returning_user()

        elif isinstance(user, str):
            bid_login = self.click_login_register(expect='new')
            credentials = self.testsetup.credentials[user]
            bid_login.sign_in(credentials['email'], credentials['password'])

        else:
            return False

        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.is_element_visible(*self.header._account_settings_locator))

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
        from browserid.pages.complete_registration import CompleteRegistration
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

        _search_locator = (By.ID, 'search-q')
        _search_arrow_locator = (By.ID, 'search-go')
        _search_suggestions_locator = (By.CSS_SELECTOR, '#site-search-suggestions .wrap')
        _search_suggestions_list_locator = (By.CSS_SELECTOR, '#site-search-suggestions .wrap ul >li')
        _account_settings_locator = (By.CSS_SELECTOR, '.sticky')
        _sign_out_locator = (By.CSS_SELECTOR, '.logout')
        _sign_in_locator = (By.CSS_SELECTOR, 'a.browserid')

        @property
        def is_user_logged_in(self):
            return self.is_element_visible(*self._account_settings_locator)

        @property
        def search_field_placeholder(self):
            return self.selenium.find_element(*self._search_locator).get_attribute('placeholder')

        def hover_over_settings_menu(self):
            hover_element = self.selenium.find_element(*self._account_settings_locator)
            ActionChains(self.selenium).\
                move_to_element(hover_element).\
                perform()

        def click_sign_out(self):
            self.hover_over_settings_menu
            self.selenium.find_element(*self._sign_out_locator).click()
            WebDriverWait(self.selenium, self.timeout).until(lambda s: self.is_element_visible(*self._sign_in_locator))

        def click_account_settings(self):
            self.selenium.find_element(*self._account_settings_locator).click()
            from pages.desktop.consumer_pages.account_settings import BasicInfo
            return BasicInfo(self.testsetup)

        def search(self, search_term):
            """
            Searches for an app using the available search field
            :Args:

             - search_term - string value of the search field

            :Usage:
             - search(search_term="text")
            """
            search_field = self.selenium.find_element(*self._search_locator)
            search_field.send_keys(search_term)
            search_field.submit()
            from pages.desktop.consumer_pages.search import Search
            return Search(self.testsetup)

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

        class Menu(Page):

            _menu_locator = (By.CSS_SELECTOR, 'a.menu-button')
            _menu_items_locator = (By.CSS_SELECTOR, 'ul#flyout > li')

            def open_menu(self):
                if not self.is_menu_visible:
                    self.click_menu()

            def close_menu(self):
                if self.is_menu_visible:
                    self.click_menu()

            def click_menu(self):
                """
                Click on the element that opens/closes menu
                """
                self.find_element(*self._menu_locator).click()

            def click_menu_item(self, name):
                """
                Click on a menu item.
                Arg: Label of menu item to select, ex: "Popular"
                """
                self.open_menu()
                for item in self.items:
                    if item.name == name:
                        item.click_item()
                        break

            @property
            def is_menu_visible(self):
                return self.find_element(*self._menu_items_locator).is_displayed()

            @property
            def items(self):
                return [self.MenuItem(self.testsetup, web_element)
                        for web_element in self.find_elements(*self._menu_items_locator)]

            class MenuItem (Page):

                _name_locator = (By.CSS_SELECTOR, 'a')

                def __init__(self, testsetup, web_element):
                    Page.__init__(self, testsetup)
                    self._root_element = web_element

                @property
                def name(self):
                    return self._root_element.find_element(*self._name_locator).text

                def click_item(self):
                    return self._root_element.find_element(*self._name_locator).click()

    class FooterRegion(Page):

        _account_controller_locator = (By.CSS_SELECTOR, '#site-footer > div.account.authenticated > a:nth-child(1)')
        _logout_locator = (By.CSS_SELECTOR, '#site-footer > div.account.authenticated > a.logout')

        _account_history_locator = (By.CSS_SELECTOR, '#site-footer > nav.footer-links > a:nth-child(2)')
        _account_settings_locator = (By.CSS_SELECTOR, '#site-footer > nav.footer-links > a:nth-child(3)')

        _select_language_locator = (By.ID, 'language')
        _label_for_lang_select_locator = (By.CSS_SELECTOR, '#lang-form > label')

        def click_logout(self):
            self.selenium.find_element(*self._logout_locator).click()

        def click_account_history(self):
            self.selenium.find_element(*self._account_history_locator).click()
            from pages.desktop.consumer_pages.account_history import AccountHistory
            return AccountHistory(self.testsetup)

        @property
        def currently_selected_language(self):
            select_el = self.selenium.find_element(*self._select_language_locator)
            return Select(select_el).first_selected_option.get_attribute('value')

        def switch_to_another_language(self, option_value):
            Select(self.selenium.find_element(*self._select_language_locator)).select_by_value(option_value)

        @property
        def select_lang_label_text(self):
            return self.selenium.find_element(*self._label_for_lang_select_locator).text
