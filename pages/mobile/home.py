# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.mobile.base import Base


class Home(Base):

    _page_title = "Firefox Marketplace"

    _site_navigation_footer_locator = (By.ID, 'navigation')
    _promo_box_locator = (By.CSS_SELECTOR, '.desktop-promo')

    def go_to_homepage(self):
        self.selenium.get(self.base_url)
        self.wait_for_element_present(*self._site_navigation_footer_locator)

    @property
    def is_promo_box_not_visible(self):
        return self.is_element_not_visible(*self._promo_box_locator)
