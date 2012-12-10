#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.page import Page, PageRegion


class CategoriesSection(Page):

    _category_section_title_locator = (By.CSS_SELECTOR, '.categories > h2')
    _category_item_locator = (By.CSS_SELECTOR, '.categories li')
    _category_section_locator = (By.CSS_SELECTOR, ".categories.slider.full")
    _category_slider_next_locator = (By.CSS_SELECTOR, ".categories.slider.full .next-page.show")
    _category_slider_prev_locator = (By.CSS_SELECTOR, ".categories.slider.full .prev-page.show")

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

    def slide_forward(self):
        self.selenium.find_element(*self._category_slider_next_locator).click()

    def slide_backward(self):
        self.selenium.find_element(*self._category_slider_prev_locator).click()

    @property
    def is_slide_forward_visible(self):
        return self.is_element_visible(*self._category_slider_next_locator)

    @property
    def is_slide_backward_visible(self):
        return self.is_element_visible(*self._category_slider_prev_locator)

    @property
    def is_slide_backward_not_visible(self):
        return self.is_element_not_visible(*self._category_slider_prev_locator)

    class CategoryItem(PageRegion):

        _category_name_locator = (By.CSS_SELECTOR, "a > h3")
        _category_link_locator = (By.CSS_SELECTOR, "a")

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
