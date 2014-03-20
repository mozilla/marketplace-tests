#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.page import PageRegion
from pages.mobile.base import Base


class Home(Base):

    _page_title = "Firefox Marketplace"

    _featured_section_locator = (By.ID, 'featured')
    _featured_list_locator = (By.CSS_SELECTOR, '#featured > .grid.c > li')
    _new_popular_apps_list_locator = (By.CSS_SELECTOR, 'li.item.result.app.c')
    _new_popular_view_all_locator = (By.CSS_SELECTOR, '#gallery a.view-all')
    _category_item_locator = (By.CSS_SELECTOR, '.cat-menu.cat-icons.c > li:not(:nth-child(1))')
    _category_section_locator = (By.ID, 'cat-list')
    _category_section_title_locator = (By.CSS_SELECTOR, '.cat-all.cat-icon')
    _gallery_section_locator = (By.ID, 'gallery')
    _popular_category_tab_locator = (By.CSS_SELECTOR, '.tabs > a[href*="category-popular"]')
    _new_category_tab_locator = (By.CSS_SELECTOR, '.tabs > a[href*="category-new"]')
    _loading_spinner_locator = (By.CSS_SELECTOR, '.loading > .spinner.padded.alt')

    def go_to_homepage(self):
        self.selenium.get(self.base_url)
        self.wait_for_element_present(*self._featured_section_locator)

    @property
    def is_featured_section_visible(self):
        return self.is_element_visible(*self._featured_section_locator)

    @property
    def is_gallery_section_visible(self):
        return self.is_element_visible(*self._gallery_section_locator)

    @property
    def is_category_section_visible(self):
        return self.is_element_visible(*self._category_section_locator)

    @property
    def is_popular_category_tab_visible(self):
        return self.is_element_visible(*self._popular_category_tab_locator)

    @property
    def is_new_category_tab_visible(self):
        return self.is_element_visible(*self._new_category_tab_locator)

    @property
    def is_popular_category_tab_selected(self):
        locator = self._popular_category_tab_locator
        return self.find_element(*locator).get_attribute("class") == 'active'

    @property
    def is_new_category_tab_selected(self):
        locator = self._new_category_tab_locator
        return self.find_element(*locator).get_attribute("class") == 'active'

    @property
    def featured_apps(self):
        return [self.Application(self.testsetup, web_element)
                for web_element in self.selenium.find_elements(*self._featured_list_locator)]

    @property
    def popular_apps(self):
        return [self.Application(self.testsetup, web_element)
                for web_element in self.selenium.find_elements(*self._new_popular_apps_list_locator)]

    @property
    def new_apps(self):
        return [self.Application(self.testsetup, web_element)
                for web_element in self.selenium.find_elements(*self._new_popular_apps_list_locator)]

    def expand_all_categories_section(self):
        self.selenium.find_element(*self._category_section_title_locator).click()

    def click_popular_category_tab(self):
        self.selenium.find_element(*self._popular_category_tab_locator).click()
        self.wait_for_element_not_present(*self._loading_spinner_locator)
        return self.popular_apps

    def click_new_category_tab(self):
        self.selenium.find_element(*self._new_category_tab_locator).click()
        self.wait_for_element_not_present(*self._loading_spinner_locator)
        return self.new_apps

    def click_new_popular_view_all_link(self):
        self.selenium.find_element(*self._new_popular_view_all_locator).click()
        from pages.mobile.search import Search
        search_items = Search(self.testsetup)
        self.wait_for_element_not_present(*search_items._loading_spinner_locator)
        return search_items

    @property
    def categories(self):
        return [self.CategoryItem(self.testsetup, web_element)
                for web_element in self.selenium.find_elements(*self._category_item_locator)]

    class Application(PageRegion):
            _name_locator = (By.CSS_SELECTOR, '.info > h3')
            _price_locator = (By.CSS_SELECTOR, '.price.vital')

            @property
            def name(self):
                return self.find_element(*self._name_locator).text

            @property
            def price(self):
                return self.find_element(*self._price_locator).text

            def click(self):
                self.find_element(*self._name_locator).click()
                from pages.mobile.details import Details
                return Details(self.testsetup)

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
