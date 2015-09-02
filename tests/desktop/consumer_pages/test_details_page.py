# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest

from tests.base_test import BaseTest
from pages.desktop.consumer_pages.home import Home


class TestDetailsPage(BaseTest):

    @pytest.mark.sanity
    @pytest.mark.nondestructive
    def test_that_application_page_contains_proper_objects(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        assert home_page.is_the_current_page

        search_term = self._take_first_free_app_name(mozwebqa)
        details_page = home_page.header.search_and_click_on_app(search_term)
        assert details_page.is_the_current_page
        assert search_term == details_page.app_name
        assert details_page.is_image_visible
        assert details_page.app_name == details_page.name
        assert details_page.is_app_dev_username_visible
        assert details_page.is_install_button_visible
        assert details_page.is_support_email_visible or details_page.is_app_site_visible
        assert details_page.is_application_description_visible
        assert details_page.is_image_preview_section_visible
        assert details_page.is_privacy_policy_link_visible
        assert details_page.is_report_abuse_button_visible

    def test_that_reports_abuse_as_anonymous_user(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        assert home_page.is_the_current_page

        search_term = self._take_first_free_app_name(mozwebqa)
        details_page = home_page.header.search_and_click_on_app(search_term)
        assert details_page.is_the_current_page
        assert details_page.is_report_abuse_button_visible

        report_abuse_box = details_page.click_report_abuse_button()
        assert report_abuse_box.is_visible

        report_abuse_box.insert_text('This is an automatically generated report.')
        assert report_abuse_box.is_report_button_enabled

        report_abuse_box.click_report_button()
        details_page.wait_for_notification('Report submitted. Thanks!')

    @pytest.mark.credentials
    def test_that_reports_abuse_as_signed_in_user(self, mozwebqa, new_user):
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        assert home_page.is_the_current_page

        home_page.header.click_sign_in()
        home_page.login(new_user['email'], new_user['password'])
        assert home_page.header.is_user_logged_in

        search_term = self._take_first_free_app_name(mozwebqa)
        details_page = home_page.header.search_and_click_on_app(search_term)
        assert details_page.is_the_current_page
        assert details_page.is_report_abuse_button_visible

        report_abuse_box = details_page.click_report_abuse_button()
        assert report_abuse_box.is_visible

        report_abuse_box.insert_text('This is an automatically generated report.')
        assert report_abuse_box.is_report_button_enabled

        report_abuse_box.click_report_button()
        details_page.wait_for_notification('Report submitted. Thanks!')

    @pytest.mark.nondestructive
    def test_clicking_on_content_rating(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        assert home_page.is_the_current_page

        home_page.set_region("restofworld")
        search_term = self._take_first_free_app_name(mozwebqa)
        details_page = home_page.header.search_and_click_on_app(search_term)
        assert details_page.is_the_current_page

        details_page.wait_for_ratings_image_visible()
        content_ratings_page = details_page.click_content_ratings_button()
        assert content_ratings_page.is_the_current_page
        assert content_ratings_page.is_ratings_table_visible
