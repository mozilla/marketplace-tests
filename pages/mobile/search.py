# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.mobile.item_list import ItemList


class Search(ItemList):

    _no_results_locator = (By.CSS_SELECTOR, '.no-results')

    @property
    def no_results_text(self):
        return self.find_element(*self._no_results_locator).text
