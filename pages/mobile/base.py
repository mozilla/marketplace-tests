#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.page import Page
from pages.page import PageRegion


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
        page_locator = (By.CSS_SELECTOR, "#container > #page[data-bodyclass='%s']" % self._data_body_class)
        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.is_element_visible(*page_locator))

    @property
    def is_the_current_body_class(self):
        self.wait_for_page_to_load()
        if self.selenium.find_element(*self._body_class_locator).get_attribute('data-bodyclass') == self._data_body_class:
            return True
        return False

    @property
    def header(self):
        return self.Header(self.testsetup)

    class Header(Page):
        _settings_locator = (By.CSS_SELECTOR, '.header-button.icon.settings.left')
        _search_button_locator = (By.CSS_SELECTOR, '.header-button.icon.search.right')
        _search_locator = (By.ID, 'search-q')

        _search_suggestions_title_locator = (By.CSS_SELECTOR, '#site-search-suggestions div.wrap > p > a > span')
        _search_suggestions_locator = (By.ID, 'site-search-suggestions')
        _search_suggestion_locator = (By.CSS_SELECTOR, '#site-search-suggestions > div.wrap > ul > li')

        def click_settings(self):
            self.selenium.find_element(*self._settings_locator).click()
            from pages.mobile.settings import Account
            return Account(self.testsetup)

        def click_search(self):
            self.selenium.find_element(*self._search_button_locator).click()
            self.wait_for_element_present(*self._search_locator)

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
