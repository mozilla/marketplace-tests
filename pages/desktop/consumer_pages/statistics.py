#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.page import Page
from pages.desktop.consumer_pages.base import Base


class Statistics(Base):

        _page_title = "Statistics Dashboard"
        _chart_locator = (By.CSS_SELECTOR, 'div.highcharts-container')
        _table_data = (By.CSS_SELECTOR, 'table > tbody > tr:nth-child(1) > th')
        _next_locator = (By.CSS_SELECTOR, 'p.rel a.button.next')
        _prev_locator = (By.CSS_SELECTOR, 'p.rel a.button.prev')
        _prev_disabled_locator = (By.CSS_SELECTOR, 'p.rel a.button.prev.disabled')
        _next_button_locator = (By.CSS_SELECTOR, "p.rel a.button.next")
        _prev_button_locator = (By.CSS_SELECTOR, "p.rel a.button.prev")

        def click_on_link(self, *locator):
                self.selenium.find_element(*locator).click()
                from pages.desktop.consumer_pages.statistics import Statistics
                return Statistics(self.testsetup)

        @property
        def is_chart_visible(self):
                return self.is_element_visible(*self._chart_locator)

        @property
        def verify_report_start(self):
                import datetime

                now = datetime.datetime.now()
                yesterday = now - datetime.timedelta(days=1)
                data = self.get_text_from_location(*self._table_data)
                day_yesterday_num = yesterday.day
                day_now_num = now.day
                _date_yesterday = yesterday.strftime("%a, %b" + " %d," % day_yesterday_num + " %Y")
                _date_today = now.strftime("%a, %b" + " %d," % day_now_num + " %Y")
                if ((data == _date_yesterday) or (data == _date_today)):
                        return True
                else:
                        return False

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
                return self.click_on_link(*self._next_locator)

        def click_prev_button(self):
                return self.click_on_link(*self._prev_locator)
