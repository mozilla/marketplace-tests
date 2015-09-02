#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.mobile.home import Home


class TestDetails():

    @pytest.mark.nondestructive
    def test_details_page_for_an_app(self, mozwebqa):
        """https://moztrap.mozilla.org/runtests/run/243/env/112/ - Verify details page for an app"""
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        details_page = home_page.go_to_first_free_app_page()
        assert details_page.header.is_back_button_visible
        assert details_page.is_author_visible
        assert details_page.is_app_icon_present
        assert details_page.is_rating_visible
        assert details_page.is_product_details_visible
        assert details_page.is_description_visible

    @pytest.mark.xfail(reason='Bug 1156370 - Create some fake apps which have all the optional fields listed')
    @pytest.mark.nondestructive
    def test_reviews_section(self, mozwebqa):
        """https://moztrap.mozilla.org/runtests/run/243/env/112/ - Verify details page for an app - Reviews section"""
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        details_page = home_page.go_to_first_free_app_page()

        # This takes the number of reviews on the details page and based on that number it treats 3 different scenarios:
        # when the app has reviews, when it has 1 review and when the app isn't rated.
        if details_page.is_app_rated:
            reviews_count = details_page.reviews_count
            reviews = details_page.reviews
            if reviews_count >= 2:
                if len(reviews) == 2:
                    for review in reviews:
                        assert review.is_visible
            elif reviews_count == 1:
                assert reviews[0].is_visible
        else:
            assert 'App not yet rated' == details_page.app_not_rated_text

        assert details_page.is_write_a_review_button_visible

        for support_button in details_page.support_buttons_list:
            assert details_page.is_element_visible(*support_button)
