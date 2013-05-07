#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By

from pages.page import Page, PageRegion


class CategoriesSection(Page):

    _category_section_title_locator = (By.CSS_SELECTOR, '.cat-all.cat-icon')
    _category_item_locator = (By.CSS_SELECTOR, '.cat-icons.c > li:not(:nth-child(1))')

    @property
    def title(self):
        return self.selenium.find_element(*self._category_section_title_locator).text

    @property
    def is_title_visible(self):
        return self.is_element_visible(*self._category_section_title_locator)

    @property
    def items(self):
        return [self.CategoryItem(self.testsetup, web_element)
                for web_element in self.selenium.find_elements(*self._category_item_locator)]

    class CategoryItem(PageRegion):

        _category_name_locator = (By.CSS_SELECTOR, '.cat-icons.c > li:not(:nth-child(1)) a')
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
