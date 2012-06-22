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
	_next_locator = (By.CSS_SELECTOR, 'p.rel a.button.next')
	_prev_locator = (By.CSS_SELECTOR, 'p.rel a.button.prev')
	_prev_disabled_locator = (By.CSS_SELECTOR, 'p.rel a.button.prev.disabled')
	_reports_csv_locator = (By.CSS_SELECTOR, 'h2>span #export_data_csv')
	_reports_json_locator = (By.CSS_SELECTOR, 'h2>span #export_data_json')
	_table_data = (By.CSS_SELECTOR, 'table>tbody>tr:nth-child(1)>th')
	_range_seven_inactive = (By.CSS_SELECTOR,'.criteria.range.island>ul>li>a.week.inactive')
	_range_thirty_inactive = (By.CSS_SELECTOR,'.criteria.range.island>ul>li>a.month.inactive')
	@property
	def is_chart_visible(self):
		return self.is_element_visible(*self._chart_locator)
	@property
	def seven_is_disabled(self):
		return self.is_element_visible(*self._range_seven_inactive)
	@property
	def thirty_is_disabled(self):
		return self.is_element_visible(*self._range_month_inactive)
	@property
	def is_prev_disabled(self):
		return self.is_element_visible(*self._prev_disabled_locator)
	
	@property
	def is_prev_visible(self):
		return self.is_element_visible(*self._prev_locator)
	
	@property
	def is_next_visible(self):
		return self.is_element_visible(*self._next_locator)
		
	@property
	def is_reports_csv_visible(self):
		return self.is_element_visible(*self._reports_csv_locator)

	@property
	def is_reports_json_visible(self):
		return self.is_element_visible(*self._reports_json_locator)
		
	@property
	def verify_report_start(self):
		import datetime
		now = datetime.datetime.now()
		yest = now - datetime.timedelta(days=1)
		data = self.get_text_from_location(*self._table_data)
		
		_date_yest = yest.strftime("%a, %b %d, %Y")
		_date_today = now.strftime("%a, %b %d, %Y")
		print str(_date_today)
		print str(_date_yest)
		
		if (data == _date_yest) or (data == _date_today):
			return True
		else:
			return False
	