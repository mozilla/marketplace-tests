#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By

from pages.page import PageRegion
from pages.desktop.consumer_pages.base import Base
from pages.desktop.regions.sorter import Sorter
from pages.desktop.regions.filter import Filter


class Search(Base, Sorter, Filter):
    """
    Consumer search page

    https://marketplace-dev.allizom.org/
    """

    _expand_button_locator = (By.CSS_SELECTOR, '.expand-toggle')
    _results_locator = (By.CSS_SELECTOR, '#search-results .item.result.app')
    _applied_filters_locator = (By.CSS_SELECTOR, '.applied-filters > ol > li > a')
    _search_results_section_title_locator = (By.CSS_SELECTOR, '.secondary-header.c > h2')
    _search_results_section_locator = (By.ID, 'search-results')

    def __init__(self, testsetup, app_name=False):
        Base.__init__(self, testsetup)
        Sorter.__init__(self, testsetup)
        if app_name:
            self._page_title = '%s | Firefox Marketplace' % app_name
            self.app_name = app_name
        else:
            self._page_title = 'Search Results | Firefox Marketplace'
        self.wait_for_element_present(*self._search_results_section_locator)

    @property
    def applied_filters(self):
        return self.find_element(*self._applied_filters_locator).text

    @property
    def search_results_section_title(self):
        return self.find_element(*self._search_results_section_title_locator).text

    def click_on_expand_button(self):
        self.find_element(*self._expand_button_locator).click()

    @property
    def results(self):
        return [self.SearchResult(self.testsetup, web_element)
                for web_element in self.find_elements(*self._results_locator)]

    class SearchResult(PageRegion):
        """provides the methods to access a search result
        self._root_element - webelement that points to a single result"""

        _screenshots_locator = (By.CSS_SELECTOR, '.screenshot')
        _install_button_locator = (By.CSS_SELECTOR, '.button.install')
        _rating_locator = (By.CSS_SELECTOR, '.stars.large.stars')
        _reviews_number_locator = (By.CSS_SELECTOR, '.cnt.long')
        _icon_locator = (By.CSS_SELECTOR, '.icon')
        _name_locator = (By.CSS_SELECTOR, '.info > h3')
        _categories_locator = (By.CSS_SELECTOR, 'div.info > div.vitals.c > span.vital:nth-child(2)')

        @property
        def screenshots_visible(self):
            return self.find_element(*self._screenshots_locator).is_displayed()

        @property
        def install_button_visible(self):
            return self.find_element(*self._install_button_locator).is_displayed()

        @property
        def ratings_visible(self):
            return self.find_element(*self._rating_locator).is_displayed()

        @property
        def reviews_number_visible(self):
            return self.find_element(*self._reviews_number_locator).is_displayed()

        @property
        def name(self):
            return self.find_element(*self._name_locator).text

        @property
        def icon_visible(self):
            return self.find_element(*self._icon_locator).is_displayed()

        @property
        def categories(self):
            return self.find_element(*self._categories_locator).text

        def click_name(self):
            name = self.name
            self.find_element(*self._name_locator).click()
            from pages.desktop.consumer_pages.details import Details
            return Details(self.testsetup, name, first_access=True)
