#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.desktop.consumer_pages.base import Base


class Category(Base):

    """Category page"""

    _page_title = 'Firefox Marketplace'
    _category_section_title_locator = (By.CSS_SELECTOR, '.desktop-cat-header')
    _category_items_locator = (By.CSS_SELECTOR, '.item.result.app')

    def __init__(self, testsetup, category_name):
        Base.__init__(self, testsetup)
        self.wait_for_page_to_load()
        WebDriverWait(self.selenium, self.timeout).until(lambda s: category_name.title() == self.category_title)
        WebDriverWait(self.selenium, self.timeout).until(lambda s: len(self.apps_count) > 0)
        self._page_title = "%s | %s" % (category_name.title(), self._page_title)

    @property
    def category_title(self):
        self.wait_for_element_visible(*self._category_section_title_locator)
        return self.selenium.find_element(*self._category_section_title_locator).text

    @property
    def apps_count(self):
        return self.selenium.find_elements(*self._category_items_locator)

    @property
    def categories(self):
        from pages.desktop.regions.categories import CategoriesSection
        return CategoriesSection(self.testsetup)
