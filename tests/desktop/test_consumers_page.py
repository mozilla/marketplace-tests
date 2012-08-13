#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest

from unittestzero import Assert

from pages.desktop.consumer_pages.home import Home


class TestConsumerPage:

    @pytest.mark.nondestructive
    @pytest.mark.xfail(reason="Event triggering issue on menu close")
    def test_that_header_menu_has_expected_items(self, mozwebqa):
        """
        Verify the menu opens & closes.  Verify menu item names
        """

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.false(home_page.header.menu.is_menu_visible, "Menu open at page open")

        # open menu and verify visibility
        home_page.header.menu.open_menu()
        Assert.true(home_page.header.menu.is_menu_visible, "Menu is not open")

        # verify menu item names
        expected_menu = ["Home", "Popular", "Top Free", "Top Paid", "Categories"]
        Assert.equal(expected_menu, [ item.name for item in home_page.header.menu.items ],
                     "Unexpected menu item")

        # close menu and verify
        home_page.header.menu.close_menu()
        Assert.false(home_page.header.menu.is_menu_visible, "Menu did not close")

    @pytest.mark.nondestructive
    def test_that_verifies_the_most_popular_section(self, mozwebqa):
        '''https://www.pivotaltracker.com/projects/477093 ID:31913803'''

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.true(home_page.is_the_current_page)

        # Check if the most popular section title is visible
        Assert.true(home_page.is_most_popular_section_title_visible)

        # Check if the most popular section is visible and contains applications
        Assert.true(home_page.is_most_popular_section_visible)
        for element in home_page.popular_section_elements_list:
            if element in home_page.popular_section_elements_list[:-1]:
                Assert.true(element.is_displayed())
            else:
                Assert.false(home_page.popular_section_elements_list[-1].is_displayed())

    @pytest.mark.xfail(reason='Bug 763701 - Add region support to the featured apps tool')
    @pytest.mark.nondestructive
    def test_that_verifies_featured_application_section(self, mozwebqa):
        '''https://www.pivotaltracker.com/projects/477093 ID:31913881'''

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.true(home_page.is_the_current_page)

        # Check if featured application section title is visible
        Assert.true(home_page.is_featured_section_title_visible)

        # Check if featured section is visible and contains applications
        Assert.true(home_page.is_featured_section_visible)
        Assert.equal(home_page.featured_section_elements_count, 3)

    @pytest.mark.nondestructive
    def test_that_checks_changing_language_on_home_page(self, mozwebqa):
        """Test for https://www.pivotaltracker.com/story/show/33702365"""

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        before_lang_change = [home_page.get_url_current_page(),
                            home_page.page_title,
                            home_page.featured_section_title_text,
                            home_page.most_popular_section_title_text,
                            home_page.categories.title,
                            home_page.header.search_field_placeholder,
                            home_page.footer.select_lang_label_text]

        home_page.footer.switch_to_another_language('ru')

        after_lang_change = [home_page.get_url_current_page(),
                            home_page.page_title,
                            home_page.featured_section_title_text,
                            home_page.most_popular_section_title_text,
                            home_page.categories.title,
                            home_page.header.search_field_placeholder,
                            home_page.footer.select_lang_label_text]

        Assert.not_equal(before_lang_change, after_lang_change)

    @pytest.mark.nondestructive
    def test_that_verifies_categories_section(self, mozwebqa):
        """https://www.pivotaltracker.com/story/show/31913855"""

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.equal(home_page.categories.title, 'All categories')
        Assert.equal(len(home_page.categories.items), 15)

    @pytest.mark.nondestructive
    def test_sliding_categories_section(self, mozwebqa):
        """In addition to Pivotal #31913855"""

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        home_page.wait_for_ajax_on_page_finish()

        Assert.false(home_page.categories.is_slide_backward_visible)
        Assert.true(home_page.categories.is_slide_forward_visible)
        home_page.categories.slide_forward()

        Assert.true(home_page.categories.is_slide_backward_visible)
        Assert.true(home_page.categories.is_slide_forward_visible)

        home_page.categories.slide_backward()
        Assert.false(home_page.categories.is_slide_backward_visible)
        Assert.true(home_page.categories.is_slide_forward_visible)

    @pytest.mark.nondestructive
    def test_opening_category_page_from_categories_section(self, mozwebqa):
        """In addition to Pivotal #31913855"""

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        category_name = home_page.categories.items[3].name
        category_page = home_page.categories.items[3].click_category()

        Assert.equal(category_page.breadcrumbs[2].text, category_name)
        Assert.true(category_page.is_the_current_page)
        Assert.contains(category_name.replace(' & ', '-').lower(), category_page.get_url_current_page() )
        Assert.equal(category_page.title, category_name)
