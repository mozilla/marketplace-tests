#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest

from unittestzero import Assert

from tests.base_test import BaseTest
from pages.desktop.consumer_pages.home import Home


class TestConsumerPage(BaseTest):

    @pytest.mark.nondestructive
    def test_that_promo_module_is_visible(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.true(home_page.is_promo_box_visible)
        Assert.greater(home_page.promo_box_items_number, 0)

    @pytest.mark.sanity
    @pytest.mark.action_chains
    @pytest.mark.nondestructive
    def test_that_header_has_expected_items(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.true(home_page.header.is_logo_visible)
        Assert.true(home_page.header.is_search_visible)
        Assert.equal(home_page.header.search_field_placeholder, u'Search Marketplace\u2026')
        Assert.true(home_page.header.is_sign_in_visible)

    @pytest.mark.sanity
    @pytest.mark.nondestructive
    def test_that_verifies_categories_menu(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.equal(home_page.categories.title, 'Categories')

        home_page.open_categories_menu()
        Assert.greater(len(home_page.categories.items), 0)

    @pytest.mark.sanity
    @pytest.mark.nondestructive
    def test_opening_category_pages_from_categories_menu(self, mozwebqa):
        """Open the first 3 category pages and check the first 3 apps on those pages."""

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        categories = home_page.categories.items
        # only check the first three categories
        for c in range(3):
            home_page.open_categories_menu()
            category = categories[c]
            category_name = category.name
            category_page = category.click_category()
            Assert.equal(category_name.title(), category_page.category_title)
            Assert.true(category_page.is_the_current_page)
            apps = category_page.apps
            Assert.true(len(apps) > 0)
            Assert.true(category_page.is_new_popular_tabs_visible)
            Assert.true(category_page.popular_tab_class == 'active')

            # only check the first three apps in the category
            for a in range(3):
                app = apps[a]
                Assert.true(app.is_name_visible)
                Assert.true(app.is_icon_visible)
                Assert.true(app.is_rating_visible)
                Assert.true(app.is_install_visible)

    @pytest.mark.sanity
    @pytest.mark.nondestructive
    def test_that_verifies_nav_menu_tabs(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        home_page.click_new_tab()
        Assert.equal('New', home_page.feed_title_text)
        Assert.true(home_page.apps_are_visible)
        Assert.true(home_page.elements_count > 0)

        home_page.click_popular_tab()
        Assert.equal('Popular', home_page.feed_title_text)
        Assert.true(home_page.apps_are_visible)
        Assert.true(home_page.elements_count > 0)

    @pytest.mark.sanity
    @pytest.mark.nondestructive
    def test_settings_dropdown_menu(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        home_page.header.click_sign_in()
        acct = self.get_user(mozwebqa)
        home_page.login(acct)

        # Verify account settings menu
        user_settings = home_page.header.click_edit_account_settings()
        Assert.true(user_settings.is_the_current_page)
        Assert.true(user_settings.is_email_visible)
        Assert.true(user_settings.is_display_name_visible)
        Assert.true(user_settings.is_region_field_visible)
        Assert.true(user_settings.is_save_button_visible)
        Assert.true(user_settings.is_sign_out_button_visible)

        # Verify My Apps menu
        home_page.go_to_homepage()
        my_apps_page = home_page.header.click_my_apps()
        Assert.true(my_apps_page.is_the_current_page)
        my_apps_page.click_expand_button()
        for i in range(len(my_apps_page.apps)):
            Assert.true(my_apps_page.apps[i].are_screenshots_visible)

    @pytest.mark.sanity
    @pytest.mark.credentials
    @pytest.mark.nondestructive
    def test_footer_has_expected_items(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        home_page.header.click_sign_in()

        acct = self.get_user(mozwebqa)
        home_page.login(acct)

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
        acct = self.get_user(mozwebqa)
        home_page.login(acct)

        bad_links = []
        for link in Home.FooterRegion.footer_links_list:
            url = home_page.link_destination(link.get('locator'))
            if not url.endswith(link.get('url_suffix')):
                bad_links.append('%s does not end with %s' % (url, link.get('url_suffix')))
        Assert.equal(0, len(bad_links), '%s bad links found: ' % len(bad_links) + ', '.join(bad_links))
