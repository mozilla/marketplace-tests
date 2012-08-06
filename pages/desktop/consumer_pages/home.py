#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.page import Page
from pages.desktop.consumer_pages.base import Base


class Home(Base):

    _page_title = "Mozilla Marketplace"
    _popular_locator = (By.CSS_SELECTOR, "#home-popular a")
    _popular_list_locator = (By.CSS_SELECTOR, ".promo-grid .content")
    _popular_section_list_locator = (By.CSS_SELECTOR, ".popular.grid.full[data-group='popular'] .promo-grid .content > li")
    _featured_section_title_locator = (By.CSS_SELECTOR, "#home-featured > div > h2")
    _featured_section_locator = (By.CSS_SELECTOR, ".featured.full.slider .promo-slider .content li")

    _category_item_locator = (By.CSS_SELECTOR, ".categories.slider.full li")
    _category_section_locator = (By.CSS_SELECTOR, ".categories.slider.full")
    _category_slider_next_locator = (By.CSS_SELECTOR, ".next-page")
    _category_slider_prev_locator = (By.CSS_SELECTOR, ".prev-page")

    def go_to_homepage(self):
        self.selenium.get(self.base_url)
        self.maximize_window()

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
    def is_featured_section_title_visible(self):
        return self.is_element_visible(*self._featured_section_title_locator)

    @property
    def is_featured_section_visible(self):
        return self.is_element_visible(*self._featured_section_locator)

    @property
    def featured_section_elements_count(self):
        return len(self.selenium.find_elements(*self._featured_section_locator))

    @property
    def category_items(self):
        return [self.CategoryItem(self.testsetup, web_element)
                for web_element in self.selenium.find_elements(*self._category_item_locator)]

    def scroll_category_slider_forward(self):
        self.selenium.find_element(*self._category_slider_next_locator).click()

    def scroll_category_slider_backward(self):
        self.selenium.find_element(*self._category_slider_prev_locator).click()

    @property
    def is_category_slider_forward_visible(self):
        return self.is_element_visible(*self._category_slider_next_locator)

    @property
    def is_category_slider_backward_visible(self):
        return self.is_element_visible(*self._category_slider_prev_locator)

    class CategoryItem(Page):

        _category_name = (By.CSS_SELECTOR, "a > h3")
        _category_link = (By.CSS_SELECTOR, "a")

        def __init__(self, testsetup, web_element):
                Page.__init__(self, testsetup)
                self._root_element = web_element

        @property
        def name(self):
            return self._root_element.find_element(*self._category_name).text

        @property
        def link_to_category_page(self):
            return self._root_element.find_element(*self._category_link).get_attribute("href")
