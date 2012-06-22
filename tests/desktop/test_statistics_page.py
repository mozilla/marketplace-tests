#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from selenium.common.exceptions import InvalidElementStateException
from unittestzero import Assert

from pages.desktop.consumer_pages.home import Home

class TestStatistics:
    
    
        
        
        @pytest.mark.nondestructive
        def test_statistics_graph_is_visible(self, mozwebqa):

            	search_term = "Evernote"


		home_page = Home(mozwebqa)
		home_page.go_to_homepage()

		search_page = home_page.header.search(search_term)

		evernote_details = search_page.results[0].click_name()


		statistics_page = evernote_details.click_statistics()

		Assert.true(statistics_page.is_chart_visible)
                Assert.true(statistics_page.is_reports_csv_visible)
                Assert.true(statistics_page.is_reports_json_visible)
    
        @pytest.mark.nondestructive
        def test_next_report_navigation(self,mozwebqa):
            
            search_term = "Evernote"
            i = 0
    
            home_page = Home(mozwebqa)
	    home_page.go_to_homepage()
	    search_page = home_page.header.search(search_term)
	    evernote_details = search_page.results[0].click_name()
	    statistics_page = evernote_details.click_statistics()
            Assert.true(statistics_page.is_prev_disabled)
            
            for i in range(0,10):
                next_report = statistics_page.click_next_button()
                Assert.true(statistics_page.is_prev_visible)   
                Assert.false(statistics_page.is_prev_disabled)
        
            for i in range(0,10):
                next_report = statistics_page.click_prev_button()
                Assert.true(statistics_page.is_prev_visible) 
            Assert.true(statistics_page.is_prev_disabled)
            
        
        @pytest.mark.nondestructive
        def test_report_date_validity(self,mozwebqa):
            """
            Checks the First Date of the report is todays date or yesterdays date
            """

            search_term = "Evernote"
    
            home_page = Home(mozwebqa)
            home_page.go_to_homepage()
            search_page = home_page.header.search(search_term)
            evernote_details = search_page.results[0].click_name()
            statistics_page = evernote_details.click_statistics()

            Assert.true(statistics_page.verify_report_start)
        
        @pytest.mark.xfail(reason="bug 767079")
        @pytest.mark.nondestructive
        def test_all_options_for_sorting_chart(self,mozwebqa):
            """
            Checks all the options for sorting the graph
            """
            search_term = "Evernote"
            home_page = Home(mozwebqa)
            home_page.go_to_homepage()
            search_page = home_page.header.search(search_term)
            evernote_details = search_page.results[0].click_name()
            statistics_page = evernote_details.click_statistics()
            sorted_page[1] = statistics_page
            
            for i in range(2, 4):
                _link_locator_for_type[i] = (By.CSS_SELECTOR,'.criteria.stat-type.island>ul>li:nth-of-type(%d)>a'%i)
                sorted_page[i] = sorted_page[i-1].click_on_link(*self._link_locator_for_type[i])
                for j in range(2, 4):
                    _link_locator_for_group_by[j] = (By.CSS_SELECTOR,'.criteria.group.island>ul>li:nth-of-type(%d)>a'%j)
                    sorted_page_group[j] = sorted_page[i].click_on_link(*self._link_locator_for_group_by[j])
                    for k in range(2,5):
                        _link_locator_for_last[k] = (By.CSS_SELECTOR,'.criteria.range.island>ul>li:nth-of-type(%d)>a'%j)
                        sorted_page_range[j] = sorted_page_group[j].click_on_link(*self._link_locator_for_last[k])
                        if(j>2):
                            Assert.true(sorted_page_range[j].seven_is_disabled)
                        if(j>3):
                            Assert.true(sorted_page_range[j].thirty_is_disabled)
                        
                        if ((((j == 3) or (j == 4)) and(k == 2)) or((j == 4)and(k == 3))):
                            Assert.false(statistics_page.is_chart_visible)
                        else:
                            Assert.true(statistics_page.is_chart_visible)
                        
                        
                        
                        
                        
                        