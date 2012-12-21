#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from pages.page import Page


class Filter(Page):
    _results_count_tag = (By.CSS_SELECTOR, '#search-results .listing li.item')

    @property
    def results_count(self):
        return len(self.selenium.find_elements(*self._results_count_tag))

    def filter_by(self, lookup):
        return self.Tag(self.testsetup, lookup)

    class FilterResults(Page):

        _item_link = (By.CSS_SELECTOR, ' a')
        _all_tags_locator = (By.CSS_SELECTOR, '#search-facets > ul.facets.island.pjax-trigger > li.facet')

        def __init__(self, testsetup, lookup):
            Page.__init__(self, testsetup)

            # expand the thing here to represent the proper user action
            self._root_element = self.selenium.find_element(self._base_locator[0],
                                    "%s/ul/li/a[normalize-space(text())='%s']" % (self._base_locator[1], lookup))

        @property
        def name(self):
            return self._root_element.text

        @property
        def is_selected(self):
            return "selected" in self._root_element.get_attribute('class')

        def click(self):
            self._root_element.click()
            WebDriverWait(self.selenium, 10).until(lambda s: self.is_element_visible(By.CSS_SELECTOR, ".applied-filters>ol>li>a"))
