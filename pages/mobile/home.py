#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.page import PageRegion
from pages.mobile.base import Base


class Home(Base):

    _page_title = "Firefox Marketplace"

    _site_navigation_menu_locator = (By.ID, 'site-nav')
    _home_page_app_list_locator = (By.CSS_SELECTOR, '.app-link.c')
    _new_popular_apps_list_locator = (By.CSS_SELECTOR, '.app-list li')
    _categories_menu_tab_locator = (By.CSS_SELECTOR, '.categories .tab-link')
    _category_item_locator = (By.CSS_SELECTOR, '.category-index a')
    _category_section_locator = (By.CSS_SELECTOR, '.category-index')
    _homepage_menu_locator = (By.CSS_SELECTOR, '.homepage')
    _popular_menu_tab_locator = (By.CSS_SELECTOR, '.popular a')
    _new_menu_tab_locator = (By.CSS_SELECTOR, '.new a')
    _loading_spinner_locator = (By.CSS_SELECTOR, '.loading')
    _first_new_app_name_locator = (By.CSS_SELECTOR, '.app-name:nth-child(1)')
    _tabs_locator = (By.CSS_SELECTOR, '.navbar a')
    _feed_title_locator = (By.CSS_SELECTOR, '.feed-tile-header')

    def go_to_homepage(self):
        self.selenium.get(self.base_url)
        self.wait_for_element_present(*self._site_navigation_menu_locator)

    @property
    def is_nav_menu_visible(self):
        return self.is_element_visible(*self._site_navigation_menu_locator)

    @property
    def is_category_section_visible(self):
        return self.is_element_visible(*self._category_section_locator)

    @property
    def is_popular_category_tab_visible(self):
        return self.is_element_visible(*self._popular_menu_tab_locator)

    @property
    def is_new_category_tab_visible(self):
        return self.is_element_visible(*self._new_menu_tab_locator)

    @property
    def home_page_apps(self):
        return [self.Application(self.testsetup, web_element)
                for web_element in self.selenium.find_elements(*self._home_page_app_list_locator)]

    @property
    def popular_apps(self):
        return [self.Application(self.testsetup, web_element)
                for web_element in self.selenium.find_elements(*self._new_popular_apps_list_locator)]

    @property
    def new_apps(self):
        return [self.Application(self.testsetup, web_element)
                for web_element in self.selenium.find_elements(*self._new_popular_apps_list_locator)]

    @property
    def first_app_name(self):
        return self.find_element(*self._first_new_app_name_locator).text

    def open_categories_menu(self):
        self.selenium.find_element(*self._categories_menu_tab_locator).click()

    def click_popular_menu_tab(self):
        self.selenium.find_element(*self._popular_menu_tab_locator).click()
        self.wait_for_element_not_present(*self._loading_spinner_locator)
        return self.popular_apps

    def click_new_menu_tab(self):
        self.selenium.find_element(*self._new_menu_tab_locator).click()

    @property
    def feed_title_text(self):
        return self.find_element(*self._feed_title_locator).text

    @property
    def categories(self):
        return [self.CategoryItem(self.testsetup, web_element)
                for web_element in self.selenium.find_elements(*self._category_item_locator)]

    class Application(PageRegion):

            _name_locator = (By.CSS_SELECTOR, '.app-name')
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
