#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.page import PageRegion
from pages.mobile.base import Base


class Search(Base):

    _result_locator = (By.CSS_SELECTOR, '.item.result.app.c')
    _no_results_locator = (By.CSS_SELECTOR, '#search-results .no-results')
    _loading_spinner_locator = (By.CSS_SELECTOR, '.loading > .spinner.spaced.alt')
    _last_result_item_locator = (By.CSS_SELECTOR, '#search-results li:last-of-type')
    _more_button_locator = (By.CSS_SELECTOR, "#search-results .loadmore")

    @property
    def no_results_text(self):
        return self.find_element(*self._no_results_locator).text

    @property
    def results(self):
        results = self.find_elements(*self._result_locator)
        return [self.Result(self.testsetup, result) for result in results]

    @property
    def is_more_button_visible(self):
        return self.is_element_visible(*self._more_button_locator)

    def scroll_to_last_result_item(self):
        self.scroll_to_element(*self._last_result_item_locator)

    class Result(PageRegion):
        _name_locator = (By.CSS_SELECTOR, "div.info > h3")

        @property
        def name(self):
            return self.find_element(*self._name_locator).text

        def click_app(self):
            self.selenium.find_element(*self._name_locator).click()
            from pages.mobile.details import Details
            return Details(self.testsetup)
