#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from pages.desktop.consumer_pages.base import Base


class Home(Base):

    _page_title = 'Firefox Marketplace'
    _site_navigation_menu_locator = (By.ID, 'site-nav')
    _category_menu_locator = (By.CSS_SELECTOR, '.categories .desktop-cat-link')
    _category_count_locator = (By.CSS_SELECTOR, '.categories li')
    _first_app_locator = (By.CSS_SELECTOR, '#featured > ol > li:first-child > a')
    _gallery_section_locator = (By.CLASS_NAME, 'gallery')
    _item_locator = (By.CSS_SELECTOR, '.app.mini-app')
    _selected_tab_locator = (By.CSS_SELECTOR, '.navbar .active')
    _tabs_locator = (By.CSS_SELECTOR, '.navbar a')
    _view_all_locator = (By.CLASS_NAME, 'view-all')
    _first_new_app_name_locator = (By.CSS_SELECTOR, '.app-name:nth-child(1)')

    def go_to_homepage(self):
        self.selenium.get(self.base_url)
        self.maximize_window()
        self.wait_for_element_visible(*self._site_navigation_menu_locator)

    @property
    def category_menu_text(self):
        return self.selenium.find_element(*self._category_menu_locator).text

    def hover_over_categories_menu(self):
        hover_element = self.selenium.find_element(*self._category_menu_locator)
        ActionChains(self.selenium).\
        move_to_element(hover_element).\
        perform()

    @property
    def categories(self):
        from pages.desktop.regions.categories import CategoriesSection
        return CategoriesSection(self.testsetup)

    @property
    def category_count(self):
        return len(self.selenium.find_elements(*self._category_count_locator))

    @property
    def first_new_app_name(self):
        return self.find_element(*self._first_new_app_name_locator).text

    @property
    def apps_are_visible(self):
        return self.is_element_visible(*self._item_locator)

    @property
    def elements_count(self):
        return len(self.find_elements(*self._item_locator))

    @property
    def selected_tab_text(self):
        return self.find_element(*self._selected_tab_locator).text

    def click_new_tab(self):
        if 'Home'.upper() == self.selected_tab_text:
            self.find_elements(*self._tabs_locator)[1].click()
        else:
            self.find_elements(*self._tabs_locator)[2].click()
