#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from pages.mobile.home import Home


class TestHomepage():

    @pytest.mark.nondestructive
    def test_that_promo_module_not_present_on_mobile(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.true(home_page.is_promo_box_not_visible)

    @pytest.mark.nondestructive
    def test_that_verifies_categories_menu(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        categories = home_page.nav_menu.click_categories()
        Assert.greater(len(categories.categories), 0)

    @pytest.mark.nondestructive
    def test_switch_between_new_and_popular_pages(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        popular_apps = home_page.nav_menu.click_popular()
        Assert.equal('Popular', home_page.feed_title_text)
        Assert.true(len(popular_apps) > 0)

        new_apps = home_page.nav_menu.click_new()
        Assert.equal('New', home_page.feed_title_text)
        Assert.true(len(new_apps) > 0)
