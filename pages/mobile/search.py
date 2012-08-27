#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.page import PageRegion
from pages.mobile.base import Base


class Search(Base):

    _data_body_class = "search"

    _result_locator = (By.CSS_SELECTOR, '#search-results > ol.listing > li.item')

    @property
    def results(self):
        results = self.find_elements(*self._result_locator)
        return [self.Result(self.testsetup, result) for result in results]

    class Result(PageRegion):
        pass
