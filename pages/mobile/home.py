#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.page import PageRegion
from pages.mobile.base import Base


class Home(Base):

    _page_title = "Firefox Marketplace"

    _featured_section_locator = (By.ID, 'featured-home')
    _featured_list_locator = (By.CSS_SELECTOR, 'section.featured > ul.grid > li')
    _category_item_locator = (By.CSS_SELECTOR, 'section.categories > ul > li')
    _category_section_locator = (By.CSS_SELECTOR, '.categories')

    def go_to_homepage(self):
        self.selenium.get(self.base_url)
        self.wait_for_element_present(*self._featured_section_locator)

    @property
    def is_featured_section_visible(self):
        return self.is_element_visible(*self._featured_section_locator)

    @property
    def featured_section_elements_count(self):
        return len(self.selenium.find_elements(*self._featured_list_locator))

    @property
    def is_category_section_visible(self):
        return self.is_element_visible(*self._category_section_locator)

    @property
    def first_featured_app_name(self):
        return self.selenium.find_element(self._featured_list_locator[0], (self._featured_list_locator[1] + ':nth-child(1) a h3')).text

    def click_first_featured_app(self):
        self.selenium.find_element(self._featured_list_locator[0], (self._featured_list_locator[1] + ':nth-child(1)')).click()
        from pages.mobile.details import Details
        return Details(self.testsetup)

    @property
    def categories(self):
        return [self.CategoryItem(self.testsetup, web_element)
                for web_element in self.selenium.find_elements(*self._category_item_locator)]

    class CategoryItem(PageRegion):

        _category_name_locator = (By.CSS_SELECTOR, 'a > h3')
        _category_link_locator = (By.CSS_SELECTOR, 'a')

        @property
        def name(self):
            return self.find_element(*self._category_name_locator).text

        @property
        def link_to_category_page(self):
            return self.find_element(*self._category_link_locator).get_attribute("href")

        def click_category(self):
            category_name = self.name
            self.find_element(*self._category_link_locator).click()
            from pages.desktop.consumer_pages.category import Category
            return Category(self.testsetup, category_name)
