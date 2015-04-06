#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.desktop.consumer_pages.base import Base


class Home(Base):

    _page_title = 'Firefox Marketplace'

    _site_navigation_menu_locator = (By.CSS_SELECTOR, '.navbar')
    _category_menu_locator = (By.CSS_SELECTOR, '.tab-categories')
    _category_count_locator = (By.CSS_SELECTOR, '.cat-overlay li')
    _item_locator = (By.CSS_SELECTOR, '.app-list-app')
    _categories_tabel_locator = (By.CSS_SELECTOR, '.cat-overlay')
    _first_new_app_name_locator = (By.CSS_SELECTOR, '.info > h3')
    _new_tab_menu_locator = (By.CSS_SELECTOR, '.tab-link[href*=new]')
    _popular_tab_menu_locator = (By.CSS_SELECTOR, '.tab-link[href*=popular]')
    _feed_title_locator = (By.CSS_SELECTOR, '.subheader > h1')
    _promo_box_locator = (By.CSS_SELECTOR, '.desktop-promo')
    _promo_box_items_locator = (By.CSS_SELECTOR, '.desktop-promo-item')

    def go_to_homepage(self):
        self.set_window_size()
        self.selenium.get(self.base_url)
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: self.selenium.execute_script('return jQuery.isReady == true'))
        self.wait_for_element_visible(*self._site_navigation_menu_locator)

    @property
    def is_promo_box_visible(self):
        return self.is_element_visible(*self._promo_box_locator)

    @property
    def promo_box_items_number(self):
        return len(self.find_elements(*self._promo_box_items_locator))

    @property
    def category_menu_text(self):
        return self.selenium.find_element(*self._category_menu_locator).text

    def hover_over_categories_menu(self):
        while self.is_element_not_visible(*self._categories_tabel_locator):
            hover_element = self.selenium.find_element(*self._category_menu_locator)
            ActionChains(self.selenium).move_to_element(hover_element).perform()

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

    def click_new_tab(self):
        self.scroll_to_element(*self._new_tab_menu_locator)
        self.find_element(*self._new_tab_menu_locator).click()

    def click_popular_tab(self):
        self.find_element(*self._popular_tab_menu_locator).click()

    def click_homepage_tab(self):
        self.find_element(*self._new_tab_menu_locator).click()

    @property
    def feed_title_text(self):
        return self.find_element(*self._feed_title_locator).text
