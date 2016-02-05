# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.mobile.home import Home


class TestHomepage():

    @pytest.mark.nondestructive
    def test_that_promo_module_not_present_on_mobile(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        home_page.go_to_homepage()
        assert home_page.is_promo_box_not_visible

    @pytest.mark.nondestructive
    def test_that_verifies_categories_menu(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        home_page.go_to_homepage()
        page = home_page.click_apps()
        categories = page.click_categories()
        assert len(categories.categories) > 0

    @pytest.mark.nondestructive
    def test_switch_between_new_and_popular_pages(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        home_page.go_to_homepage()
        page = home_page.click_apps()
        page.click_popular()
        assert page.is_popular_selected
        assert len(page.items()) > 0

        page.click_new()
        assert page.is_new_selected
        assert len(page.items()) > 0
