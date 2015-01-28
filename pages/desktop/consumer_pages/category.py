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

    _popular_tab_locator = (By.CSS_SELECTOR, '.app-list-sort a:nth-child(1)')
    _new_popular_tabs_locator = (By.CSS_SELECTOR, '.app-list-sort a')
    _category_section_title_locator = (By.CSS_SELECTOR, '.subheader > h1')
    _category_apps_locator = (By.CSS_SELECTOR, '.item.result.app-list-app')

    def __init__(self, testsetup, category_name):
        Base.__init__(self, testsetup)
        self.wait_for_page_to_load()
        WebDriverWait(self.selenium, self.timeout).until(lambda s: category_name.title() == self.category_title)
        WebDriverWait(self.selenium, self.timeout).until(lambda s: len(self.apps) > 0)
        self._page_title = "%s | %s" % (category_name.title(), self._page_title)

    @property
    def category_title(self):
        self.wait_for_element_visible(*self._category_section_title_locator)
        return self.selenium.find_element(*self._category_section_title_locator).text

    @property
    def popular_tab_class(self):
        return self.selenium.find_element(*self._popular_tab_locator).get_attribute('class')

    @property
    def is_new_popular_tabs_visible(self):
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
        _app_install_locator = (By.CSS_SELECTOR, '.install')
        _app_rating_locator = (By.CSS_SELECTOR, '.stars')

        @property
        def is_name_visible(self):
            return self.is_element_visible(*self._app_name_locator)

        @property
        def is_icon_visible(self):
            return self.is_element_visible(*self._app_icon_locator)

        @property
        def is_rating_visible(self):
            return self.is_element_visible(*self._app_rating_locator)

        @property
        def is_install_visible(self):
            return self.is_element_visible(*self._app_install_locator)
