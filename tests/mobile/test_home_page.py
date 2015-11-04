# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.mobile.home import Home


class TestHomepage():

    @pytest.mark.nondestructive
    def test_that_promo_module_not_present_on_mobile(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        assert home_page.is_promo_box_not_visible

    @pytest.mark.nondestructive
    def test_that_verifies_categories_menu(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        categories = home_page.more_menu.click_categories()
        assert len(categories.categories) > 0

    @pytest.mark.nondestructive
    def test_switch_between_new_and_popular_pages(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        popular_apps = home_page.more_menu.click_popular()
        assert 'Popular' == home_page.feed_title_text
        assert len(popular_apps) > 0

        new_apps = home_page.more_menu.click_new()
        assert 'New' == home_page.feed_title_text
        assert len(new_apps) > 0
