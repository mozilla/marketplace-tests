#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.desktop.consumer_pages.base import Base


class Home(Base):

    _page_title = "Mozilla Marketplace"
    _popular_locator = (By.CSS_SELECTOR, "#home-popular a")
    _popular_list_locator = (By.CSS_SELECTOR, ".promo-grid .content")

    def go_to_homepage(self):
        self.selenium.get(self.base_url)
        self.maximize_window()

    @property
    def is_most_popular_section_title_visible(self):
        return self.is_element_visible(*self._popular_locator)

    @property
    def is_most_popular_section_visible(self):
        return self.is_element_visible(*self._popular_list_locator)
