#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.desktop.consumer_pages.base import Base


class Home(Base):

    _page_title = 'Firefox Marketplace'
    _popular_locator = (By.CSS_SELECTOR, "#home-popular a")
    _popular_list_locator = (By.CSS_SELECTOR, ".promo-grid .content")
    _popular_section_list_locator = (By.CSS_SELECTOR, ".popular.grid.full[data-group='popular'] .promo-grid .content > li")
    _featured_section_title_locator = (By.CSS_SELECTOR, "#home-featured > div > h2")
    _featured_section_locator = (By.CSS_SELECTOR, '#featured-home > ul > li')
    _category_count_locator = (By.CSS_SELECTOR, '.categories > ul li')
    _first_app_locator = (By.CSS_SELECTOR, '#featured-home > ul > li:nth-child(1) > a')

    def go_to_homepage(self):
        self.selenium.get(self.base_url)
        self.maximize_window()

    @property
    def most_popular_section_title_text(self):
        return self.selenium.find_element(*self._popular_locator).text

    @property
    def is_most_popular_section_title_visible(self):
        return self.is_element_visible(*self._popular_locator)

    @property
    def is_most_popular_section_visible(self):
        return self.is_element_visible(*self._popular_list_locator)

    @property
    def popular_section_elements_list(self):
        return self.selenium.find_elements(*self._popular_section_list_locator)

    @property
    def featured_section_title_text(self):
        return self.selenium.find_element(*self._featured_section_title_locator).text

    @property
    def is_featured_section_title_visible(self):
        return self.is_element_visible(*self._featured_section_title_locator)

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
