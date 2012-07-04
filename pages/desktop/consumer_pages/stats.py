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
        _range_seven_inactive = (By.CSS_SELECTOR, '.criteria.range.island>ul>li>a.week.inactive')
        _range_thirty_inactive = (By.CSS_SELECTOR, '.criteria.range.island>ul>li>a.month.inactive')
        _group_week_inactive = (By.CSS_SELECTOR, '.criteria.group.island>ul>li:nth-child(3)>a.inactive')
        _group_month_inactive = (By.CSS_SELECTOR, '.criteria.group.island>ul>li:nth-child(4)>a.inactive')
        _stats_range_sorting = [(By.CSS_SELECTOR, '.criteria.range.island>ul>li:nth-child(2)>a'), (By.CSS_SELECTOR, '.criteria.range.island>ul>li:nth-child(3)>a'), (By.CSS_SELECTOR, '.criteria.range.island>ul>li:nth-child(4)>a'), (By.CSS_SELECTOR, '.criteria.range.island>ul>li:nth-child(5)>a')]
        _stats_type_sorting = [(By.CSS_SELECTOR, '.criteria.stat-type.island>ul>li:nth-child(2)>a'), (By.CSS_SELECTOR, '.criteria.stat-type.island>ul>li:nth-child(3)>a'), (By.CSS_SELECTOR, '.criteria.stat-type.island>ul>li:nth-child(4)>a')]
        _stats_group_sorting = [(By.CSS_SELECTOR, '.criteria.group.island>ul>li:nth-child(2)>a'), (By.CSS_SELECTOR, '.criteria.group.island>ul>li:nth-child(3)>a'), (By.CSS_SELECTOR, '.criteria.group.island>ul>li:nth-child(4)>a')]

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
                day_yest_num = yest.day
                day_now_num = now.day
                _date_yest = yest.strftime("%a, %b" + " %d," % day_yest_num + " %Y")
                _date_today = now.strftime("%a, %b" + " %d," % day_now_num + " %Y")
                if ((data == _date_yest) or (data == _date_today)):
                        return True
                else:
                        return False

        @property
        def is_seven_deactive(self):
                return self.is_element_visible(*self._range_seven_inactive)

        @property
        def is_week_deactive(self):
                return self.is_element_visible(*self._group_week_inactive)

        @property
        def is_month_deactive(self):
                return self.is_element_visible(*self._group_month_inactive)

        @property
        def is_thirty_deactive(self):
                return self.is_element_visible(*self._range_thirty_inactive)

        @property
        def verify_sorting_option_30days(self):

                i = 0
                for i in range(0, 3):
                        page_loaded_type = self.click_on_link(*self._stats_type_sorting[i])
                        page_loaded_group_day = page_loaded_type.click_on_link(*self._stats_group_sorting[0])
                        if(not(page_loaded_group_day.is_thirty_deactive)):
                                sorted_30day_page = page_loaded_group_day.click_on_link(*self._stats_range_sorting[1])
                                if(not(sorted_30day_page.is_seven_deactive)):
                                        if(not(sorted_30day_page.is_week_deactive)and(sorted_30day_page.is_month_deactive)):
                                                if(sorted_30day_page.is_chart_visible):
                                                        continue
                                                else:
                                                        return False
                                        else:
                                                return False
                                else:
                                        return False
                        else:
                                return False
                return True

        @property
        def verify_sorting_option_7days(self):

                i = 0
                for i in range(0, 3):
                        page_loaded_type = self.click_on_link(*self._stats_type_sorting[i])
                        page_loaded_group_day = page_loaded_type.click_on_link(*self._stats_group_sorting[0])
                        if(not(page_loaded_group_day.is_seven_deactive)):
                                sorted_7day_page = page_loaded_group_day.click_on_link(*self._stats_range_sorting[0])
                                if(not(sorted_7day_page.is_seven_deactive)):
                                        if((sorted_7day_page.is_week_deactive)and(sorted_7day_page.is_month_deactive)):
                                                if(sorted_7day_page.is_chart_visible):
                                                        continue
                                                else:
                                                        return False
                                        else:
                                                return False
                                else:
                                        return False
                        else:
                                return False
                return True

        @property
        def verify_sorting_option_30week(self):

                i = 0
                for i in range(0, 3):
                        page_loaded_type = self.click_on_link(*self._stats_type_sorting[i])
                        page_loaded_group = page_loaded_type.click_on_link(*self._stats_group_sorting[0])
                        if(not(page_loaded_group.is_thirty_deactive)):
                                sorted_30day_page = page_loaded_group.click_on_link(*self._stats_range_sorting[1])
                                if(not(sorted_30day_page.is_seven_deactive)):
                                        sorted_30day_page_week = sorted_30day_page.click_on_link(*self._stats_group_sorting[1])
                                        if(not(sorted_30day_page_week.is_week_deactive)and(sorted_30day_page_week.is_month_deactive)and(sorted_30day_page_week.is_seven_deactive)):
                                                if(sorted_30day_page_week.is_chart_visible):
                                                        continue
                                                else:
                                                        return False
                                        else:
                                                return False
                                else:
                                        return False
                        else:
                                return False
                return True

        @property
        def verify_sorting_option_90days(self):

                i = 0
                for i in range(0, 3):
                        page_loaded_type = self.click_on_link(*self._stats_type_sorting[i])
                        page_loaded_group_day = page_loaded_type.click_on_link(*self._stats_group_sorting[0])
                        if(not(page_loaded_group_day.is_thirty_deactive)):
                                sorted_90day_page = page_loaded_group_day.click_on_link(*self._stats_range_sorting[2])
                                if(not(sorted_90day_page.is_seven_deactive)):
                                        if(not(sorted_90day_page.is_week_deactive)and(not(sorted_90day_page.is_month_deactive))):
                                                if(sorted_90day_page.is_chart_visible):
                                                        continue
                                                else:
                                                        return False
                                        else:
                                                return False
                                else:
                                        return False
                        else:
                                return False
                return True

        @property
        def verify_sorting_option_90week(self):

                i = 0
                for i in range(0, 3):
                        page_loaded_type = self.click_on_link(*self._stats_type_sorting[i])
                        page_loaded_group_day = page_loaded_type.click_on_link(*self._stats_group_sorting[0])
                        if(not(page_loaded_group_day.is_thirty_deactive)):
                                sorted_90day_page = page_loaded_group_day.click_on_link(*self._stats_range_sorting[2])
                                if(not(sorted_90day_page.is_seven_deactive)):
                                        sorted_90day_page_week = sorted_90day_page.click_on_link(*self._stats_group_sorting[1])
                                        if(not(sorted_90day_page_week.is_week_deactive)and(not(sorted_90day_page_week.is_month_deactive))and(sorted_90day_page_week.is_seven_deactive)):
                                                if(not(sorted_90day_page_week.is_thirty_deactive)):
                                                        if(sorted_90day_page_week.is_chart_visible):
                                                                continue
                                                        else:
                                                                return False
                                                else:
                                                        return False
                                        else:
                                                return False
                                else:
                                        return False
                        else:
                                return False
                return True

        @property
        def verify_sorting_option_90month(self):

                i = 0
                for i in range(0, 3):
                        page_loaded_type = self.click_on_link(*self._stats_type_sorting[i])
                        page_loaded_group_day = page_loaded_type.click_on_link(*self._stats_group_sorting[0])
                        if(not(page_loaded_group_day.is_thirty_deactive)):
                                sorted_90day_page = page_loaded_group_day.click_on_link(*self._stats_range_sorting[2])
                                if(not(sorted_90day_page.is_seven_deactive)):
                                        sorted_90day_page_month = sorted_90day_page.click_on_link(*self._stats_group_sorting[2])
                                        if(not(sorted_90day_page_month.is_week_deactive)and(not(sorted_90day_page_month.is_month_deactive))and(sorted_90day_page_month.is_seven_deactive)):
                                                if(sorted_90day_page_month.is_thirty_deactive):
                                                        if(sorted_90day_page_month.is_chart_visible):
                                                                continue
                                                        else:
                                                                return False
                                                else:
                                                        return False
                                        else:
                                                return False
                                else:
                                        return False
                        else:
                                return False
                return True

        @property
        def verify_sorting_option_365days(self):

                i = 0
                for i in range(0, 3):
                        page_loaded_type = self.click_on_link(*self._stats_type_sorting[i])
                        page_loaded_group_day = page_loaded_type.click_on_link(*self._stats_group_sorting[0])
                        if(not(page_loaded_group_day.is_thirty_deactive)):
                                sorted_365day_page = page_loaded_group_day.click_on_link(*self._stats_range_sorting[3])
                                if(not(sorted_365day_page.is_seven_deactive)):
                                        if(not(sorted_365day_page.is_week_deactive)and(not(sorted_365day_page.is_month_deactive))):
                                                if(sorted_365day_page.is_chart_visible):
                                                        continue
                                                else:
                                                        return False
                                        else:
                                                return False
                                else:
                                        return False
                        else:
                                return False
                return True

        @property
        def verify_sorting_option_365week(self):

                i = 0
                for i in range(0, 3):
                        page_loaded_type = self.click_on_link(*self._stats_type_sorting[i])
                        page_loaded_group_day = page_loaded_type.click_on_link(*self._stats_group_sorting[0])
                        if(not(page_loaded_group_day.is_thirty_deactive)):
                                sorted_365day_page = page_loaded_group_day.click_on_link(*self._stats_range_sorting[3])
                                if(not(sorted_365day_page.is_seven_deactive)):
                                        sorted_365day_page_week = sorted_365day_page.click_on_link(*self._stats_group_sorting[1])
                                        if(not(sorted_365day_page_week.is_week_deactive)and(not(sorted_365day_page_week.is_month_deactive))and(sorted_365day_page_week.is_seven_deactive)):
                                                if(not(sorted_365day_page_week.is_thirty_deactive)):
                                                        if(sorted_365day_page_week.is_chart_visible):
                                                                continue
                                                        else:
                                                                return False
                                                else:
                                                        return False
                                        else:
                                                return False
                                else:
                                        return False
                        else:
                                return False
                return True

        @property
        def verify_sorting_option_365month(self):

                i = 0
                for i in range(0, 3):
                        page_loaded_type = self.click_on_link(*self._stats_type_sorting[i])
                        page_loaded_group_day = page_loaded_type.click_on_link(*self._stats_group_sorting[0])
                        if(not(page_loaded_group_day.is_thirty_deactive)):
                                sorted_365day_page = page_loaded_group_day.click_on_link(*self._stats_range_sorting[3])
                                if(not(sorted_365day_page.is_seven_deactive)):
                                        sorted_365day_page_month = sorted_365day_page.click_on_link(*self._stats_group_sorting[2])
                                        if(not(sorted_365day_page_month.is_week_deactive)and(not(sorted_365day_page_month.is_month_deactive))and(sorted_365day_page_month.is_seven_deactive)):
                                                if(sorted_365day_page_month.is_thirty_deactive):
                                                        if(sorted_365day_page_month.is_chart_visible):
                                                                continue
                                                        else:
                                                                return False
                                                else:
                                                        return False
                                        else:
                                                return False
                                else:
                                        return False
                        else:
                                return False
                return True
