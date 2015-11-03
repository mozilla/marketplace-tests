# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.desktop.consumer_pages.base import Base


class Home(Base):

    _page_title = 'Firefox Marketplace'

    _site_navigation_menu_locator = (By.CSS_SELECTOR, 'mkt-header-nav')
    _item_locator = (By.CSS_SELECTOR, '.app-list-app')
    _first_app_name_locator = (By.CSS_SELECTOR, '.app-list .mkt-product-name')
    _new_tab_menu_locator = (By.CSS_SELECTOR, '#navigation li a.new')
    _popular_tab_menu_locator = (By.CSS_SELECTOR, '#navigation li a.popular')
    _feed_title_locator = (By.CSS_SELECTOR, '.subheader > h1')

    def go_to_homepage(self):
        self.set_window_size()
        self.selenium.get(self.base_url)
        self.wait_for_page_to_load()

    @property
    def first_app_name(self):
        return self.find_element(*self._first_app_name_locator).text

    @property
    def apps_are_visible(self):
        return self.is_element_visible(*self._item_locator)

    @property
    def elements_count(self):
        return len(self.find_elements(*self._item_locator))

    def click_new_tab(self):
        new_tab_menu = self.selenium.find_element(*self._new_tab_menu_locator)
        self.scroll_to_element(new_tab_menu)
        new_tab_menu.click()

    def click_popular_tab(self):
        self.find_element(*self._popular_tab_menu_locator).click()

    def click_homepage_tab(self):
        self.find_element(*self._new_tab_menu_locator).click()

    @property
    def feed_title_text(self):
        return self.find_element(*self._feed_title_locator).text
