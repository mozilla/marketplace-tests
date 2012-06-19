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

	@property
	def is_chart_visible(self):
        	return self.is_element_visible(*self._chart_locator)
                                                               
