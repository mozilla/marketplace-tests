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

    @property
    def page_title(self):
        WebDriverWait(self.selenium, 10).until(lambda s: self.selenium.title)
        return self.selenium.title

    def wait_for_ajax_on_page_finish(self):
        WebDriverWait(self.selenium, self.timeout).until(lambda s: not self.is_element_present(*self._loading_balloon_locator)
                                                         and self.selenium.execute_script('return jQuery.active == 0'))

    def wait_for_page_to_load(self):
        """waits for the correct page to load
        we have to provide the value of  #container > #page[data-bodyclass] locator
        in the specific class for this method to work
        """
        WebDriverWait(self.selenium, self.timeout).until(lambda s: '"bodyclass": "%s"' % self._data_body_class in
                                                                   self.selenium.find_element(By.ID, 'page').get_attribute('data-context'))

    @property
    def is_the_current_page(self):
        """#container > #page[data-context] locator contains information about the content of the current page.
        The bodyclass property can be used to identify the current page.
        Overrides the Page.is_the_current_page method
        """
        self.wait_for_page_to_load()
        if '"bodyclass": "%s"' % self._data_body_class in self.selenium.find_element(*self._body_class_locator).get_attribute('data-context'):
            return True
        return False

    def login_with_user(self, user="default"):
        """Logins to page using the provided user"""

        bid_login = self.footer.click_login_register()
        self.selenium.execute_script('localStorage.clear()')
        credentials = self.testsetup.credentials[user]
        bid_login.sign_in(credentials['email'], credentials['password'])

        self.footer.wait_for_login_not_present()

    def search_for(self, search_term):
        if self.header.is_search_button_visible:
            self.header.click_search()

        Assert.true(self.header.is_search_visible)
        self.header.type_in_search_field(search_term)
        self.header.submit_search()
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
        _back_button_locator = (By.ID, 'nav-back')

        def click_back(self):
            self.selenium.find_element(*self._back_button_locator).click()

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
            return  self.is_element_visible(*self._login_locator)

        def wait_for_login_not_present(self):
            self.wait_for_element_not_present(*self._login_locator)
