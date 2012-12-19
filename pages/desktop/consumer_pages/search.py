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
    _page_title = 'Search | Firefox Marketplace'
    _title_locator = (By.CSS_SELECTOR, "#search-results > h1")
    _results_locator = (By.CSS_SELECTOR, '#search-results li.item')
    _applied_filters_locator = (By.CSS_SELECTOR, '.applied-filters > ol > li > a')

    def __init__(self, testsetup, search_term=False):
        Base.__init__(self, testsetup)
        Sorter.__init__(self, testsetup)
        if search_term and search_term is not "":
            self._page_title = "%s | %s" % (search_term, self._page_title)

    @property
    def applied_filters(self):
        return self.find_element(*self._applied_filters_locator).text

    @property
    def title(self):
        return self.find_element(*self._title_locator).text

    @property
    def results(self):
        return [self.SearchResult(self.testsetup, web_element)
                for web_element in self.find_elements(*self._results_locator)]

    class SearchResult(PageRegion):
        """provides the methods to access a search result
        self._root_element - webelement that points to a single result"""

        _name_locator = (By.CSS_SELECTOR, 'div.info > h3')
        _price_locator = (By.CSS_SELECTOR, "div.info > div.vitals.c > span.vital.price")
        _categories_locator = (By.CSS_SELECTOR, "div.info > div.vitals.c > span.vital:nth-child(2)")
        _devices_locator = (By.CSS_SELECTOR, "div.actions > .device-list.c > ul > li")

        @property
        def name(self):
            return self.find_element(*self._name_locator).text

        @property
        def price(self):
            return self.find_element(*self._price_locator).text

        @property
        def categories(self):
            return self.find_element(*self._categories_locator).text

        @property
        def available_devices(self):
            """Returns a list of the devices available:

            ex: ["Desktop", Tablet]"""

            device_list = []
            devices = self.find_elements(*self._devices_locator)
            for device in devices:
                if not "unavailable" in device.get_attribute("class"):
                    device_list.append(device.text)
            return device_list

        def click_name(self):
            name = self.name
            self.find_element(*self._name_locator).click()
            from pages.desktop.consumer_pages.details import Details
            return Details(self.testsetup, name)
