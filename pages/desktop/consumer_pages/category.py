#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By

from pages.page import PageRegion
from pages.desktop.consumer_pages.base import Base


class Category(Base):


    """Category page"""
    
    _page_title = "Mozilla Marketplace"
    _title_locator = (By.CSS_SELECTOR, ".sticky")
    _popular_section_title_locator = (By.CSS_SELECTOR, ".see-all.c > a > span")
    _popular_section_see_all_locator = (By.CSS_SELECTOR, ".see-all.c > a > em")
    _popular_section_locator = (By.CSS_SELECTOR, ".popular.grid.full")
    _popular_section_item_locator = (By.CSS_SELECTOR, ".popular.grid.full li")

    def __init__(self, testsetup, category_name):
        Base.__init__(self, testsetup)
        self._page_title = "%s | %s" % (category_name, self._page_title)

    @property
    def title(self):
        return self.find_element(*self._title_locator).text

    @property
    def categories(self):
        from pages.desktop.regions.categories import CategoriesSection
        return CategoriesSection(self.testsetup)

    def click_see_all_link(self):
        self.selenium.find_element(*self._popular_section_see_all_locator)

    @property
    def is_popular_section_visible(self):
        return self.is_element_visible(*self._popular_section_locator)

    @property
    def is_popular_section_title_visible(self):
        return self.is_element_visible(*self._popular_section_title_locator)

    @property
    def popular_section_title_text(self):
        return self.selenium.find_element(*self._popular_section_title_locator).text

    @property
    def popular_section_items(self):
        return [self.PopSectionItem(self.testsetup, web_element)
                for web_element in self.selenium.find_elements(*self._popular_section_item_locator)]

    class PopSectionItem(PageRegion):


        _app_image_locator = (By.CSS_SELECTOR, ".img.icon")
        _app_name_locator = (By.CSS_SELECTOR, ".product.mkt-tile.arrow > h3")
        _app_price_locator = (By.CSS_SELECTOR, ".price")
        _app_author_locator = (By.CSS_SELECTOR, ".author")
        _app_rating_locator = (By.CSS_SELECTOR, ".rating")

        @property
        def image(self):
            return self._root_element.find_element(_app_image_locator)

        @property
        def name(self):
            return self._root_element.find_element(_app_name_locator)

        @property
        def price(self):
            return self._root_element.find_element(_app_price_locator)

        @property
        def rating(self):
            return self._root_element.find_element(_app_rating_locator)

        @property
        def author(self):
            return self._root_element.find_element(_app_author_locator)

        def click_app(self):
            app_name = self.name
            self._root_element.click()
            from pages.desktop.consumer_pages.details import Details
            return Details(self.testsetup, app_name)
