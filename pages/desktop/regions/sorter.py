#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.page import Page


class Sorter(Page):

    _sort_by_relevancy_locator = (By.CSS_SELECTOR, '.relevancy > a')
    _sort_by_rating_locator = (By.CSS_SELECTOR, '.rating > a')

    _selected_sort_by_locator = (By.CSS_SELECTOR, '#filter-sort a.sel')
    _sorter_header_locator = (By.CSS_SELECTOR, '#filter-sort')

    _loading_balloon_locator = (By.CSS_SELECTOR, ".items")

    @property
    def is_sorter_header_visible(self):
        return self.is_element_visible(*self._sorter_header_locator)

    def sort_by(self, type):
        """
        Method that accesses the sort region in the search results page
        :Args:
         - type - sort type that will be applied.
                 Available sort options: "Relevancy", "Rating"

         :Usage:
          - sort_by("Revelancy")
        """
        click_element = self.selenium.find_element(*getattr(self, '_sort_by_%s_locator' % type.replace(' ', '_').lower()))
        click_element.click()
        WebDriverWait(self.selenium, 10).until(lambda s: self.selenium.execute_script("return jQuery.active == 0"))

    @property
    def sorted_by(self):
        return self.selenium.find_element(*self._selected_sort_by_locator).text
