#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By

from pages.page import Page
from pages.desktop.consumer_pages.base import Base


class Search(Base):
    """
    Consumer search page

    https://marketplace-dev.allizom.org//
    """
    _page_title = "Search | Mozilla Marketplace"
    _results_locator = (By.CSS_SELECTOR, "#search-listing > ol.items > li.item")

    def __init__(self, testsetup, search_term=False):
        Base.__init__(self, testsetup)
        if search_term:
            self._page_title = "%s | %s" % (search_term, self._page_title)

    @property
    def results(self):
        return [self.SearchResult(self.testsetup, web_element)
                for web_element in self.selenium.find_elements(*self._results_locator)]

    class SearchResult(Page):
        """provides the methods to access a search result
        self._root_element - webelement that points to a single result"""

        _name_locator = (By.CSS_SELECTOR, "div.info > h3 > a")

        def __init__(self, testsetup, element):
            Page.__init__(self, testsetup)
            self._root_element = element

        @property
        def name(self):
            return self._root_element.find_element(*self._name_locator).text

        def click_name(self):
            self._root_element.find_element(*self._name_locator).click()
            from pages.desktop.consumer_pages.details import Details
            return Details(self.testsetup, self.name)
