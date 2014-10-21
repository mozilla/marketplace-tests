#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.desktop.consumer_pages.base import Base
from pages.page import PageRegion


class Category(Base):

    """Category page"""

    _page_title = 'Firefox Marketplace'

    _view_all_link_locator = (By.CSS_SELECTOR, '.view-all')
    _popular_tab_locator = (By.CSS_SELECTOR, '.tabs a:nth-child(1)')
    _new_popular_tabs_locator = (By.CSS_SELECTOR, '.tabs a')
    _category_section_title_locator = (By.CSS_SELECTOR, '.cat-icon')
    _category_apps_locator = (By.CSS_SELECTOR, '.item.result.app')

    def __init__(self, testsetup, category_name):
        Base.__init__(self, testsetup)
        self.wait_for_page_to_load()
        WebDriverWait(self.selenium, self.timeout).until(lambda s: len(self.apps_count) > 0)
        self._page_title = "%s | %s" % (category_name.title(), self._page_title)

    @property
    def category_title(self):
        self.wait_for_element_visible(*self._category_section_title_locator)
        return self.selenium.find_element(*self._category_section_title_locator).text

    @property
    def apps_count(self):
        return self.selenium.find_elements(*self._category_apps_locator)

    @property
    def popular_tab_selected(self):
        return self.selenium.find_element(*self._popular_tab_locator).get_attribute('class')

    @property
    def view_all_link_visible(self):
        return self.is_element_visible(*self._view_all_link_locator)

    @property
    def new_popular_tabs_visible(self):
        return self.is_element_visible(*self._new_popular_tabs_locator)

    @property
    def categories(self):
        from pages.desktop.regions.categories import CategoriesSection
        return CategoriesSection(self.testsetup)

    @property
    def apps(self):
        return [self.CategoryApp(self.testsetup, web_element)
                for web_element in self.selenium.find_elements(*self._category_apps_locator)]

    class CategoryApp(PageRegion):

        _app_name_locator = (By.CSS_SELECTOR, '.info > h3')
        _app_icon_locator = (By.CSS_SELECTOR, '.icon')
        _app_price_locator = (By.CSS_SELECTOR, '.price')
        _app_rating_locator = (By.CSS_SELECTOR, '.stars')

        @property
        def name_visible(self):
            return self.is_element_visible(*self._app_name_locator)

        @property
        def icon_visible(self):
            return self.is_element_visible(*self._app_icon_locator)

        @property
        def rating_visible(self):
            return self.is_element_visible(*self._app_rating_locator)

        @property
        def price_visible(self):
            return self.is_element_visible(*self._app_price_locator)
