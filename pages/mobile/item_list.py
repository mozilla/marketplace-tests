# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import expected
from pages.page import Page, PageRegion
from pages.mobile.base import Base


class ItemList(Base):

    _item_locator = (By.CSS_SELECTOR, '.app-list .app-list-app')
    _categories_button_locator = (By.CLASS_NAME, 'header-categories-btn')
    _categories_menu_locator = (By.CLASS_NAME, 'cat-menu-overlay')
    _new_button_locator = (By.CLASS_NAME, 'sort-toggle-new')
    _popular_button_locator = (By.CLASS_NAME, 'sort-toggle-popular')
    _new_popular_data_page_type_container_locator = (By.TAG_NAME, 'body')

    @property
    def is_new_selected(self):
        return 'new' in self.selenium.find_element(
            *self._new_popular_data_page_type_container_locator).get_attribute('data-page-type')

    @property
    def is_popular_selected(self):
        return 'popular' in self.selenium.find_element(
            *self._new_popular_data_page_type_container_locator).get_attribute('data-page-type')

    def click_categories(self):
        menu = self.selenium.find_element(*self._categories_menu_locator)
        self.selenium.find_element(*self._categories_button_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(expected.element_not_moving(menu))
        return self.Categories(self.base_url, self.selenium)

    def click_new(self):
        self.selenium.find_element(*self._new_button_locator).click()

    def click_popular(self):
        self.selenium.find_element(*self._popular_button_locator).click()

    def items(self, wait_for_items=True):
        items = self.find_elements(*self._item_locator)
        if wait_for_items:
            WebDriverWait(self.selenium, self.timeout).until(lambda s: len(items) > 0)
        return [self.Item(self.base_url, self.selenium, item) for item in items]

    class Categories(Page):

        _category_item_locator = (By.CSS_SELECTOR, '.app-categories li:not(.cat-menu-all)')

        def __init__(self, base_url, selenium):
            Page.__init__(self, base_url, selenium)
            # Wait for the first category to be visible
            element = self.selenium.find_element(*self._category_item_locator)
            WebDriverWait(self.selenium, self.timeout).until(lambda s: element.is_displayed())

        @property
        def categories(self):
            return [self.CategoryItem(self.base_url, self.selenium, web_element)
                    for web_element in self.selenium.find_elements(*self._category_item_locator)]

        class CategoryItem(PageRegion):

            _category_link_locator = (By.CSS_SELECTOR, '.mkt-category-link')

            @property
            def name(self):
                return self.find_element(*self._category_link_locator).text

            @property
            def link_to_category_page(self):
                return self.find_element(*self._category_link_locator).get_attribute("href")

            def click_category(self):
                category_name = self.name
                self.find_element(*self._category_link_locator).click()
                from pages.desktop.consumer_pages.category import Category
                return Category(self.base_url, self.selenium, category_name)

    class Item(PageRegion):

        _name_locator = (By.CSS_SELECTOR, ".mkt-product-name")

        @property
        def name(self):
            return self.find_element(*self._name_locator).text

        def click(self):
            self.selenium.find_element(*self._name_locator).click()
            from pages.mobile.details import Details
            return Details(self.base_url, self.selenium)
