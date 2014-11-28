#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest

from unittestzero import Assert

from pages.desktop.consumer_pages.home import Home


class TestConsumerPage:

    @pytest.mark.sanity
    @pytest.mark.action_chains
    @pytest.mark.nondestructive
    def test_that_header_has_expected_items(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.true(home_page.header.is_logo_visible)
        Assert.true(home_page.header.is_search_visible)
        Assert.equal(home_page.header.search_field_placeholder, "Search")
        Assert.true(home_page.header.is_sign_in_visible)

    @pytest.mark.sanity
    @pytest.mark.nondestructive
    def test_that_verifies_categories_menu(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.equal(home_page.categories.title, 'Categories'.upper())

        # Hover over "Categories" menu
        home_page.hover_over_categories_menu()
        Assert.greater(len(home_page.categories.items), 0)

    @pytest.mark.sanity
    @pytest.mark.nondestructive
    def test_opening_every_category_page_from_categories_menu(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        for i in range(home_page.category_count):
            home_page.hover_over_categories_menu()
            category_name = home_page.categories.items[i].name
            category_page = home_page.categories.items[i].click_category()
            Assert.equal(category_name.title(), category_page.category_title)
            Assert.true(category_page.is_the_current_page)
            Assert.true((category_page.apps_number) > 0)
            Assert.true(category_page.is_new_popular_tabs_visible)
            Assert.true(category_page.popular_tab_class == 'active')
            Assert.true(category_page.is_view_all_link_visible)

            for i in range(category_page.apps_number):
                Assert.true(category_page.apps[i].is_name_visible)
                Assert.true(category_page.apps[i].is_icon_visible)
                Assert.true(category_page.apps[i].is_rating_visible)
                Assert.true(category_page.apps[i].is_price_visible)

    @pytest.mark.sanity
    @pytest.mark.nondestructive
    def test_that_verifies_nav_menu_tabs(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        home_page.click_new_tab()
        Assert.equal('Fresh and New Apps', home_page.feed_title_text)
        Assert.true(home_page.apps_are_visible)
        Assert.true(home_page.elements_count > 0)

        home_page.click_popular_tab()
        Assert.equal('Popular All Time', home_page.feed_title_text)
        Assert.true(home_page.apps_are_visible)
        Assert.true(home_page.elements_count > 0)

    @pytest.mark.sanity
    @pytest.mark.nondestructive
    def test_settings_dropdown_menu(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        home_page.header.click_sign_in()
        home_page.login(user="default")

        # Verify account settings menu
        user_settings = home_page.header.click_edit_account_settings()
        Assert.true(user_settings.is_the_current_page)
        Assert.true(user_settings.is_email_visible)
        Assert.true(user_settings.is_email_non_editable)
        Assert.true(user_settings.is_display_name_visible)
        Assert.true(user_settings.is_region_field_visible)
        Assert.true(user_settings.is_save_button_visible)
        Assert.true(user_settings.is_sign_out_button_visible)

        # Verify My Apps menu
        home_page.go_to_homepage()
        my_apps_page = home_page.header.click_my_apps()
        Assert.true(my_apps_page.is_the_current_page)
        my_apps_page.click_expand_button()
        for i in range(my_apps_page.my_apps_list):
            Assert.true(my_apps_page.my_apps_list[i].is_screenshots_visible)

    @pytest.mark.sanity
    @pytest.mark.credentials
    @pytest.mark.nondestructive
    def test_footer_has_expected_items(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        home_page.header.click_sign_in()
        home_page.login(user="default")

        # Inspect footer elements
        for link in home_page.footer.footer_links_list:
            link = link.get('locator')
            Assert.true(home_page.footer.is_element_visible(*link))

    @pytest.mark.sanity
    @pytest.mark.nondestructive
    def test_footer_section_links(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        home_page.header.click_sign_in()
        home_page.login(user="default")

        bad_links = []
        for link in Home.FooterRegion.footer_links_list:
            url = home_page.link_destination(link.get('locator'))
            if not url.endswith(link.get('url_suffix')):
                bad_links.append('%s does not end with %s' % (url, link.get('url_suffix')))
        Assert.equal(0, len(bad_links), '%s bad links found: ' % len(bad_links) + ', '.join(bad_links))
