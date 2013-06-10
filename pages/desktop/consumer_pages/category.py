#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By

from pages.desktop.consumer_pages.base import Base


class Category(Base):

    """Category page"""

    _page_title = 'Firefox Marketplace'
    _title_locator = (By.CSS_SELECTOR, 'title')

    def __init__(self, testsetup, category_name):
        Base.__init__(self, testsetup)
        self._page_title = "%s | %s" % (category_name, self._page_title)
        self.wait_for_page_to_load()

    @property
    def title(self):
        return self.selenium.title

    @property
    def categories(self):
        from pages.desktop.regions.categories import CategoriesSection
        return CategoriesSection(self.testsetup)
