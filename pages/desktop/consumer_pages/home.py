#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.page import PageRegion
from pages.desktop.consumer_pages.base import Base


class Home(Base):

    _page_title = 'Firefox Marketplace'
    _featured_section_locator = (By.CSS_SELECTOR, '#featured > ol > li')
    _category_section_title_locator = (By.CSS_SELECTOR, '.cat-all.cat-icon')
    _category_count_locator = (By.CSS_SELECTOR, '.cat-icons.c > li:not(:nth-child(1))')
    _first_app_locator = (By.CSS_SELECTOR, '#featured > ol > li:first-child > a')
    _gallery_section_locator = (By.CSS_SELECTOR, '#gallery')

    def go_to_homepage(self):
        self.selenium.get(self.base_url)
        self.maximize_window()
        self.wait_for_element_visible(*self._featured_section_locator)

    @property
    def is_featured_section_visible(self):
        return self.is_element_visible(*self._featured_section_locator)

    @property
    def featured_section_elements_count(self):
        return len(self.selenium.find_elements(*self._featured_section_locator))

    @property
    def category_section_title_text(self):
        return self.selenium.find_element(*self._category_section_title_locator).text

    def expand_all_categories_section(self):
        self.selenium.find_element(*self._category_section_title_locator).click()

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

    @property
    def gallery_section(self):
        section = self.find_element(*self._gallery_section_locator)
        return self.GallerySection(self.testsetup, section)

    class GallerySection(PageRegion):
        _item_locator = (By.CSS_SELECTOR, 'ol > li')
        _selected_tab_locator = (By.CSS_SELECTOR, 'nav.tabs > a.active')
        _second_tab_locator = (By.XPATH, '//nav[@class="tabs"]/a[2]')
        _view_all_locator = (By.CSS_SELECTOR, 'a.view-all')

        @property
        def is_visible(self):
            return self.is_element_visible(*self._item_locator)

        @property
        def elements_count(self):
            return len(self.find_elements(*self._item_locator))

        @property
        def selected_tab_text(self):
            return self.find_element(*self._selected_tab_locator).text

        def click_second_tab(self):
            self.find_element(*self._second_tab_locator).click()

        def click_view_all(self):
            self.find_element(*self._view_all_locator).click()
            from pages.desktop.consumer_pages.search import Search
            return Search(self.testsetup)
