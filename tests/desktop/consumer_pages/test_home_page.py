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
            Assert.true(len(category_page.apps_count) > 0)

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
    @pytest.mark.credentials
    @pytest.mark.nondestructive
    def test_footer_has_expected_items(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        home_page.login(user="default")

        # Inspect footer elements
        Assert.true(home_page.footer.is_develop_apps_button_visible)
        Assert.true(home_page.footer.is_developer_hub_link_visible)
        Assert.true(home_page.footer.is_feedback_link_visible)
        Assert.true(home_page.footer.is_region_link_visible)
        Assert.true(home_page.footer.is_my_apps_link_visible)
        Assert.true(home_page.footer.is_my_submissions_link_visible)
        Assert.true(home_page.footer.is_privacy_link_visible)
        Assert.true(home_page.footer.is_terms_link_visible)
        Assert.true(home_page.footer.is_report_abuse_link_visible)

    @pytest.mark.sanity
    @pytest.mark.nondestructive
    def test_footer_section_links(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        home_page.login(user="default")

        bad_links = []
        for link in Home.FooterRegion.footer_links_list:
            url = home_page.link_destination(link.get('locator'))
            if not url.endswith(link.get('url_suffix')):
                bad_links.append('%s does not end with %s' % (url, link.get('url_suffix')))
        Assert.equal(0, len(bad_links), '%s bad links found: ' % len(bad_links) + ', '.join(bad_links))
