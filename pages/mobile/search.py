#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.page import PageRegion
from pages.mobile.base import Base


class Search(Base):

    _result_locator = (By.CSS_SELECTOR, '.product .info')
    _no_results_locator = (By.CSS_SELECTOR, '.no-results')

    @property
    def no_results_text(self):
        return self.find_element(*self._no_results_locator).text

    def results(self, wait_for_results=True):
        results = self.find_elements(*self._result_locator)
        if wait_for_results:
            WebDriverWait(self.selenium, self.timeout).until(lambda s: len(results) > 0)
        return [self.Result(self.testsetup, result) for result in results]

    class Result(PageRegion):

        _name_locator = (By.CSS_SELECTOR, "div.info > h3")

        @property
        def name(self):
            return self.find_element(*self._name_locator).text

        def click(self):
            self.selenium.find_element(*self._name_locator).click()
            from pages.mobile.details import Details
            return Details(self.testsetup)
