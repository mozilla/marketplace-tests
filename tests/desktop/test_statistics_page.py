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


