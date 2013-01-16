#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.desktop.consumer_pages.base import Base


class Home(Base):

    _page_title = 'Firefox Marketplace'
    _featured_section_locator = (By.CSS_SELECTOR, '#featured-home > ul > li')
    _category_count_locator = (By.CSS_SELECTOR, '.categories > ul li')
    _first_app_locator = (By.CSS_SELECTOR, '#featured-home li:first-child > a')

    def go_to_homepage(self):
        self.selenium.get(self.base_url)
        self.maximize_window()

    @property
    def is_featured_section_visible(self):
        return self.is_element_visible(*self._featured_section_locator)

    @property
    def featured_section_elements_count(self):
        return len(self.selenium.find_elements(*self._featured_section_locator))

    @property
    def category_section_title_text(self):
        return self.selenium.find_element(*self._category_section_title_locator).text

    @property
    def categories(self):
        from pages.desktop.regions.categories import CategoriesSection
        return CategoriesSection(self.testsetup)

    @property
    def category_count(self):
        return len(self.selenium.find_elements(*self._category_count_locator))

    def click_on_first_app(self):
        self.selenium.find_element(*self._first_app_locator).click()
        from pages.desktop.consumer_pages.details import Details
        return Details(self.testsetup)
