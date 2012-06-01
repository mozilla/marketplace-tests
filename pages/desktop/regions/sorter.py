#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.page import Page


class Sorter(Page):

    _sort_by_relevance_locator = (By.XPATH, "//div[@id='sorter']//li/a[normalize-space(text())='Relevance']")
    _sort_by_weekly_downloads_locator = (By.XPATH, "//div[@id='sorter']//li/a[normalize-space(text())='Weekly Downloads']")
    _sort_by_top_rated_locator = (By.XPATH, "//div[@id='sorter']//li/a[normalize-space(text())='Top Rated']")
    _sort_by_price_locator = (By.XPATH, "//div[@id='sorter']//li/a[normalize-space(text())='Price']")
    _sort_by_newest_locator = (By.XPATH, "//div[@id='sorter']//li/a[normalize-space(text())='Newest']")

    _selected_sort_by_locator = (By.CSS_SELECTOR, '#sorter > ul > li.selected > a')
    _sorter_header_locator = (By.CSS_SELECTOR, "#sorter > h3")

    _loading_balloon_locator = (By.CSS_SELECTOR, ".items")

    @property
    def sorter_header(self):
        return self.selenium.find_element(*self._sorter_header_locator).text

    def sort_by(self, type):
        click_element = self.selenium.find_element(*getattr(self, '_sort_by_%s_locator' % type.replace(' ', '_').lower()))
        click_element.click()
        WebDriverWait(self.selenium, 10).until(lambda s: self.selenium.execute_script("return jQuery.active == 0"))

    @property
    def sorted_by(self):
        return self.selenium.find_element(*self._selected_sort_by_locator).text
