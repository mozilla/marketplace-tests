#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest
from unittestzero import Assert

from pages.desktop.consumer_pages.home import Home


class TestDetailsPage:
    search_term = "Hypno"

    @pytest.mark.nondestructive
    def test_that_application_page_contains_proper_objects(self, mozwebqa):
        """Moztrap 58181"""

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.true(home_page.is_the_current_page)
        search_page = home_page.header.search(self.search_term)

        # Select the first application link in the list
        details_page = search_page.results[0].click_name()
        Assert.true(details_page.is_the_current_page)

        # Check the breadcrumbs
        Assert.equal("Home", search_page.breadcrumbs[0].text)
        Assert.equal("Apps", search_page.breadcrumbs[1].text)
        Assert.equal(details_page.app_name, details_page.breadcrumbs[2].text)

        # Check the application icon
        Assert.true(details_page.is_image_visible)

        # Check application title
        Assert.equal(details_page.name, details_page.app_name)

        # Check Application Developer username
        Assert.true(details_page.app_dev_username)

        # Check the number of weekly downloads
        Assert.true(details_page.are_weekly_downloads_visible)

        # Check the section with the devices for which the application is available
        Assert.true(details_page.are_section_devices_visible)

        # Check the install/purchase button
        if (details_page.is_app_available_for_purchase):
            Assert.true(details_page.purchased_button_visible)
        else:
            Assert.true(details_page.is_install_button_visible)

        # Check the application description
        Assert.true(details_page.is_application_description_visible)

        # Check the image preview section of the application
        Assert.true(details_page.is_image_preview_section_visible)

        # Check if the support email link is visible
        Assert.true(details_page.is_support_email_visible)

        # Check if privacy policy link in visible
        Assert.true(details_page.is_privacy_policy_link_visible)

        # Check if published date is visible
        Assert.true(details_page.is_published_date_visible)

    @pytest.mark.nondestructive
    def test_navigation_buttons_for_screenshot_lightbox(self, mozwebqa):
        """
        Test for Pivotal 33702907.
        https://www.pivotaltracker.com/projects/477093#!/stories/33702907
        """
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.true(home_page.is_the_current_page)

        #Search for the test app and go to its details page
        search_page = home_page.header.search(self.search_term)
        details_page = search_page.results[0].click_name()

        images_count = details_page.previewer.image_count
        images_title = []
        image_link = []
        for img_no in range(images_count):
            images_title.append(details_page.previewer.image_title(img_no))
            image_link.append(details_page.previewer.image_link(img_no))

        image_viewer = details_page.previewer.click_image()
        Assert.true(image_viewer.is_visible)

        # Workaround: go through all list to get all images count
        for img_set in range(images_count):
            image_viewer.click_next()
        image_viewer.close()
        Assert.equal(images_count, image_viewer.images_count)

        details_page.previewer.click_image()
        for i in range(image_viewer.images_count):
            Assert.true(image_viewer.is_visible)

            Assert.equal(image_viewer.caption, images_title[i])
            Assert.equal(image_viewer.image_link(i).split('/')[-1], image_link[i].split('/')[-1])

            if not i == 0:
                Assert.true(image_viewer.is_previous_present)
            else:
                Assert.false(image_viewer.is_previous_present)

            if not i == image_viewer.images_count - 1:
                Assert.true(image_viewer.is_next_present)
                image_viewer.click_next()
            else:
                Assert.false(image_viewer.is_next_present)

        for i in range(image_viewer.images_count - 1, -1, -1):
            Assert.true(image_viewer.is_visible)

            Assert.equal(image_viewer.caption, images_title[i])
            Assert.equal(image_viewer.image_link(i).split('/')[-1], image_link[i].split('/')[-1])

            if not i == image_viewer.images_count - 1:
                Assert.true(image_viewer.is_next_present)
            else:
                Assert.false(image_viewer.is_next_present)

            if not i == 0:
                Assert.true(image_viewer.is_previous_present)
                image_viewer.click_previous()
            else:
                Assert.false(image_viewer.is_previous_present)

    @pytest.mark.nondestructive
    def test_that_checks_expanding_and_collapsing_of_app_description(self, mozwebqa):
        """Test for https://www.pivotaltracker.com/story/show/33702677"""
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        search_page = home_page.header.search('checkers')
        details_page = search_page.results[0].click_name()
        details_page.expand_app_description()

        Assert.true(details_page.is_app_description_expanded)
        Assert.greater(len(details_page.app_expanded_description_text), 0)

        details_page.collapse_app_description()

        Assert.false(details_page.is_app_description_expanded)
        Assert.false(details_page.is_app_expanded_description_visible)
