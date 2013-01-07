#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.page import Page
from pages.page import PageRegion
from unittestzero import Assert


class Base(Page):

    _loading_balloon_locator = (By.CSS_SELECTOR, '#site-header > div.loading.balloon.active')
    _body_class_locator = (By.CSS_SELECTOR, "#container > #page")
    _login_register_locator = (By.CSS_SELECTOR, 'div > p.proceed >  a.browserid')

    @property
    def page_title(self):
        WebDriverWait(self.selenium, 10).until(lambda s: self.selenium.title)
        return self.selenium.title

    def wait_for_ajax_on_page_finish(self):
        WebDriverWait(self.selenium, self.timeout).until(lambda s: not self.is_element_present(*self._loading_balloon_locator)
                                                         and self.selenium.execute_script('return jQuery.active == 0'))

    def scroll_to_element(self, *locator):
        """Scroll to element"""
        el = self.selenium.find_element(*locator)
        self.selenium.execute_script("window.scrollTo(0, %s)" % (el.location['y'] + el.size['height']))

    def login_with_user(self, user="default"):
        """Logins to page using the provided user"""

        bid_login = self.footer.click_login_register()
        self.selenium.execute_script('localStorage.clear()')
        credentials = self.testsetup.credentials[user]
        bid_login.sign_in(credentials['email'], credentials['password'])

        self.footer.wait_for_login_not_present()

    def login_with_user_from_other_pages(self, user="default"):
        self.find_element(*self._login_register_locator).click()
        from browserid.pages.sign_in import SignIn
        bid_login = SignIn(self.selenium, self.timeout)
        self.selenium.execute_script('localStorage.clear()')
        credentials = self.testsetup.credentials[user]
        bid_login.sign_in(credentials['email'], credentials['password'])

        self.wait_for_login_not_present()

    def login(self, user="default"):
        if isinstance(user, dict):
            credentials = {'email': user['email'], 'password': user['pass']}
        if isinstance(user, str):
            credentials = self.testsetup.credentials[user]

        pop_up = self.footer.click_login_register()
        pop_up.sign_in(credentials['email'], credentials['password'])
        WebDriverWait(self.selenium, self.timeout).until(lambda s: not self.footer.is_login_visible)

    def create_new_user(self):
        import urllib
        import json
        user = urllib.urlopen('http://personatestuser.org/email/').read()
        return json.loads(user)

    def wait_for_login_not_present(self):
        self.wait_for_element_not_present(*self._login_register_locator)

    def search_for(self, search_term):
        if self.header.is_search_button_visible:
            self.header.click_search()

        Assert.true(self.header.is_search_visible)
        self.header.type_in_search_field(search_term)
        self.header.submit_search()
        self.wait_for_ajax_on_page_finish()
        from pages.mobile.search import Search
        return Search(self.testsetup)

    @property
    def header(self):
        return self.Header(self.testsetup)

    @property
    def footer(self):
        return self.Footer(self.testsetup)

    class Header(Page):
        _settings_locator = (By.CSS_SELECTOR, '.header-button.icon.settings.left')
        _search_button_locator = (By.CSS_SELECTOR, '.header-button.icon.search.right')
        _search_locator = (By.ID, 'search-q')
        _search_suggestions_title_locator = (By.CSS_SELECTOR, '#site-search-suggestions div.wrap > p > a > span')
        _search_suggestions_locator = (By.ID, 'site-search-suggestions')
        _search_suggestion_locator = (By.CSS_SELECTOR, '#site-search-suggestions > div.wrap > ul > li')
        _back_button_locator = (By.CSS_SELECTOR, '#nav-back > b')

        def click_back(self):
            self.selenium.find_element(*self._back_button_locator).click()

        @property
        def is_back_button_visible(self):
            return self.is_element_visible(*self._back_button_locator)

        def click_settings(self):
            self.selenium.find_element(*self._settings_locator).click()
            from pages.mobile.settings import Account
            return Account(self.testsetup)

        def click_search(self):
            self.selenium.find_element(*self._search_button_locator).click()
            self.wait_for_element_present(*self._search_locator)

        @property
        def is_search_button_visible(self):
            return self.is_element_visible(*self._search_button_locator)

        @property
        def is_search_visible(self):
            return self.is_element_visible(*self._search_locator)

        def type_in_search_field(self, text):
            search_element = self.selenium.find_element(*self._search_locator)
            search_element.send_keys(text)

        def submit_search(self):
            search_element = self.selenium.find_element(*self._search_locator)
            search_element.submit()

        @property
        def is_search_suggestions_visible(self):
            return self.is_element_visible(*self._search_suggestions_locator)

        def wait_for_suggestions(self):
            WebDriverWait(self.selenium, 10).until(lambda s: self.is_element_visible(*self._search_suggestions_locator))

        @property
        def search_suggestions_title(self):
            return self.selenium.find_element(*self._search_suggestions_title_locator).text

        @property
        def search_suggestions(self):
            suggestions = self.selenium.find_elements(*self._search_suggestion_locator)
            return [self.SearchSuggestion(self.testsetup, suggestion) for suggestion in suggestions]

        class SearchSuggestion(PageRegion):

            _name_locator = (By.CSS_SELECTOR, 'a > span')

            @property
            def name(self):
                return self.find_element(*self._name_locator).text

            @property
            def is_icon_visible(self):
                image = self.find_element(*self._name_locator).get_attribute('style')
                return self.find_element(*self._name_locator).is_displayed() and ("background-image" in image)

    class Footer(Page):

        _footer_locator = (By.ID, 'site-footer')
        _login_locator = (By.CSS_SELECTOR, 'div.account >  a.browserid')

        @property
        def _footer(self):
            return self.selenium.find_element(*self._footer_locator)

        def click_login_register(self):
            """Click the 'Log in/Register' button.
            Keyword arguments:
            expect -- the expected resulting page
            'new' for user that is not currently signed in (default)
            'returning' for users already signed in or recently verified"""

            self._footer.click()  # we click the footer because of a android scroll issue #3171
            self._footer.find_element(*self._login_locator).click()
            from browserid.pages.sign_in import SignIn
            return SignIn(self.selenium, self.timeout)

        @property
        def is_login_visible(self):
            return self.is_element_visible(*self._login_locator)

        def wait_for_login_not_present(self):
            WebDriverWait(self.selenium, self.timeout).until(lambda s: not self.is_element_present(*self._login_locator))

        def click(self):
            self._footer.click()
