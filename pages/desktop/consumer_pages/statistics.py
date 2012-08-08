#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.page import Page
from pages.desktop.consumer_pages.base import Base
import datetime


class Statistics(Base):

        _page_title = "Statistics Dashboard"
        _chart_locator = (By.CSS_SELECTOR, 'div.highcharts-container')
        _table_data_locator = (By.CSS_SELECTOR, 'table > tbody > tr:nth-child(1) > th')
        _next_locator = (By.CSS_SELECTOR, 'p.rel a.button.next')
        _prev_locator = (By.CSS_SELECTOR, 'p.rel a.button.prev')
        _prev_disabled_locator = (By.CSS_SELECTOR, 'p.rel a.button.prev.disabled')
        _next_button_locator = (By.CSS_SELECTOR, "p.rel a.button.next")
        _prev_button_locator = (By.CSS_SELECTOR, "p.rel a.button.prev")
        _sorting_for_last_selected_link = (By.CSS_SELECTOR, ".criteria.range.island > ul > li.selected")

        @property
        def is_chart_visible(self):
                return self.is_element_visible(*self._chart_locator)

        @property
        def report_start_date(self):

                return self.selenium.find_element(*self._table_data_locator).text

        @property
        def is_prev_disabled(self):
                return self.is_element_visible(*self._prev_disabled_locator)

        @property
        def is_prev_visible(self):
                return self.is_element_visible(*self._prev_locator)

        @property
        def is_next_visible(self):
                return self.is_element_visible(*self._next_locator)

        def click_next_button(self):
                return self.selenium.find_element(*self._next_locator).click()

        def click_prev_button(self):
                return self.selenium.find_element(*self._prev_locator).click()

        def click_group_for_last(self, duration):

                for_last = duration
                self.selenium.find_element(By.LINK_TEXT, "%s" % for_last).click()
                
        def get_link_text(self, link):

                return self.selenium.find_element(By.LINK_TEXT, "%s" % link).text

        def get_selected_link(self):
                return self.selenium.find_element(*self._sorting_for_last_selected_link).text