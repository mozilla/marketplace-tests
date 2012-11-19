#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.mobile.base import Base


class Details(Base):

    _title_locator = (By.CSS_SELECTOR, 'div.info > h3')
    _write_review_locator = (By.ID, 'add-first-review')
    _product_details_locator = (By.CSS_SELECTOR, 'section.product-details')

    @property
    def _page_title(self):
        return '%s | Firefox Marketplace' % self.title

    @property
    def is_product_details_visibile(self):
        return self.is_element_visible(*self._product_details_locator)

    @property
    def title(self):
        return self.selenium.find_element(*self._title_locator).text

    def click_write_review(self):
        self.footer.click()  # we click the footer because of a android scroll issue #3171
        self.selenium.find_element(*self._write_review_locator).click()
