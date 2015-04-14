#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from mocks.mock_user import MockUser

from pages.page import Page
from pages.page import PageRegion


class Base(Page):

    _load_home_page_balloon_locator = (By.CSS_SELECTOR, '.throbber')
    _load_page_details_balloon_locator = (By.CSS_SELECTOR, '.spinner.spaced.alt')
    _body_class_locator = (By.CSS_SELECTOR, '#container > #page')
    _notification_locator = (By.ID, 'notification')
    _notification_content_locator = (By.ID, 'notification-content')

    @property
    def page_title(self):
        WebDriverWait(self.selenium, 10).until(lambda s: self.selenium.title)
        return self.selenium.title

    def wait_for_page_to_load(self):
        WebDriverWait(self.selenium, self.timeout).until(lambda s: not self.is_element_present(*self._load_page_details_balloon_locator)
                                                         and not self.is_element_visible(*self._load_home_page_balloon_locator))

    def scroll_to_element(self, *locator):
        """Scroll to element"""
        el = self.selenium.find_element(*locator)
        self.selenium.execute_script("window.scrollTo(0, %s)" % (el.location['y'] - el.size['height']))

    def search_for(self, search_term):
        self.wait_for_element_visible(*self.header._search_locator)
        self.header.type_in_search_field(search_term)
        self.header.submit_search()

        from pages.mobile.search import Search
        return Search(self.testsetup)

    def search_and_click_on_app(self, search_term):
        search_page = self.search_for(search_term)

        for i in range(len(search_page.results)):
            if search_term == search_page.results[i].name:
                return search_page.results[i].click_app()

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

    def login(self, user):
        credentials = (user, MockUser) and user
        from fxapom.pages.sign_in import SignIn
        fxa_login = SignIn(self.testsetup)
        fxa_login.sign_in(credentials['email'], credentials['password'])

    @property
    def header(self):
        return self.Header(self.testsetup)

    class Header(Page):

        _settings_button_locator = (By.CSS_SELECTOR, '.active .header-button.icon.settings')
        _search_locator = (By.ID, 'search-q')
        _search_suggestions_title_locator = (By.CSS_SELECTOR, '#site-search-suggestions div.wrap > p > a > span')
        _search_suggestions_locator = (By.ID, 'site-search-suggestions')
        _search_suggestion_locator = (By.CSS_SELECTOR, '#site-search-suggestions > div.wrap > ul > li')
        _homepage_back_button_locator = (By.CSS_SELECTOR, '.back-to-marketplace')
        _back_button_locator = (By.CSS_SELECTOR, '.header-button.back')
        _account_settings_locator = (By.CSS_SELECTOR, '.account-links > a.settings')
        _marketplace_icon_locator = (By.CSS_SELECTOR, '.wordmark')

        def click_homepage_back(self):
            self.selenium.find_element(*self._homepage_back_button_locator).click()

        def click_back(self):
            self.selenium.find_element(*self._back_button_locator).click()

        def click_marketplace_icon(self):
            self.selenium.find_element(*self._marketplace_icon_locator).click()

        @property
        def is_back_button_visible(self):
            return self.is_element_visible(*self._back_button_locator)

        def click_settings(self):
            self.selenium.find_element(*self._settings_button_locator).click()
            from pages.mobile.account_settings import AccountSettings
            return AccountSettings(self.testsetup)

        @property
        def is_account_settings_visible(self):
            return self.is_element_visible(*self._account_settings_locator)

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
