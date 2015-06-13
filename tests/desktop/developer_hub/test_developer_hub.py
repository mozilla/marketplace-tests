# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from unittestzero import Assert

from mocks.mock_application import MockApplication
from pages.desktop.developer_hub.home import Home
from tests.base_test import BaseTest


class TestDeveloperHub(BaseTest):

    def _go_to_edit_listing_page(self, mozwebqa, app):
        dev_home = Home(mozwebqa)
        edit_listing_page = dev_home.go_to_edit_listing_page(app)
        Assert.contains(app.name, edit_listing_page.page_title)
        return edit_listing_page

    @pytest.mark.credentials
    def test_that_deletes_app(self, mozwebqa, login_existing, free_app):
        edit_listing = self._go_to_edit_listing_page(mozwebqa, free_app)
        app_status_page = edit_listing.left_nav_menu.click_status()
        delete_popup = app_status_page.click_delete_app()
        my_apps = delete_popup.delete_app()
        # Set the id of the app to 0 so the global teardown won't try to delete it
        free_app['id'] = 0

        Assert.true(my_apps.is_notification_visible)
        Assert.true(my_apps.is_notification_successful, my_apps.notification_message)
        Assert.equal("App deleted.", my_apps.notification_message)

        for i in range(1, my_apps.paginator.total_page_number + 1):
            for app in my_apps.submitted_apps:
                Assert.not_equal(app.name, free_app.name)
            if my_apps.paginator.is_paginator_present:
                if not my_apps.paginator.is_first_page_disabled:
                    my_apps.paginator.click_next_page()

    @pytest.mark.credentials
    def test_that_checks_editing_basic_info_for_a_free_app(self, mozwebqa, login_existing, free_app):
        """Test the happy path for editing the basic information for a free submitted app."""

        updated_app = MockApplication(
            categories=[('Entertainment', False), ('Games', True), ('Music', True)],
        )

        edit_listing = self._go_to_edit_listing_page(mozwebqa, free_app)

        # bring up the basic info form for the first free app
        basic_info_region = edit_listing.click_edit_basic_info()

        # update the details of the app
        basic_info_region.type_url_end(updated_app['url_end'])
        basic_info_region.type_description(updated_app['description'])

        for category in updated_app['categories']:
            # check/uncheck the checkbox according to the app value
            basic_info_region.select_categories(*category)

        basic_info_region.click_save_changes()

        # check that the listing has been updated
        Assert.true(edit_listing.no_forms_are_open)
        Assert.contains(updated_app['url_end'], edit_listing.url_end)
        Assert.equal(edit_listing.description, updated_app['description'])
        Assert.equal(edit_listing.categories.sort(), updated_app['categories'].sort())

    @pytest.mark.credentials
    def test_that_checks_editing_support_information_for_a_free_app(self, mozwebqa, login_existing, free_app):
        updated_app = MockApplication()
        edit_listing = self._go_to_edit_listing_page(mozwebqa, free_app)

        # update fields in support information
        support_info_region = edit_listing.click_support_information()
        support_info_region.type_support_email(updated_app['support_email'])
        support_info_region.type_support_url(updated_app['support_website'])

        support_info_region.click_save_changes()

        # Verify the changes have been made
        Assert.equal(edit_listing.email, updated_app['support_email'])
        Assert.equal(edit_listing.website, updated_app['support_website'])

    @pytest.mark.credentials
    def test_that_checks_required_field_validations_on_basic_info_for_a_free_app(self, mozwebqa, login_existing, free_app):
        """Ensure that all required fields generate warning messages and prevent form submission."""

        edit_listing = self._go_to_edit_listing_page(mozwebqa, free_app)

        # check App URL validation
        basic_info_region = edit_listing.click_edit_basic_info()
        basic_info_region.type_url_end('')
        basic_info_region.click_save_changes()
        Assert.true(basic_info_region.is_this_form_open)
        Assert.contains('This field is required.', basic_info_region.url_end_error_message)
        basic_info_region.click_cancel()

        # check Summary validation
        basic_info_region = edit_listing.click_edit_basic_info()
        basic_info_region.type_description('')
        basic_info_region.click_save_changes()
        Assert.true(basic_info_region.is_this_form_open)
        Assert.contains('This field is required.', basic_info_region.description_error_message)
        basic_info_region.click_cancel()

    @pytest.mark.credentials
    def test_that_checks_required_field_validations_on_device_types_for_hosted_apps(self, mozwebqa, login_existing, free_app):
        edit_listing = self._go_to_edit_listing_page(mozwebqa, free_app)
        compatibility_page = edit_listing.left_nav_menu.click_compatibility_and_payments()
        compatibility_page.clear_device_types()
        compatibility_page.click_save_changes()
        Assert.contains('Please select a device.', compatibility_page.device_types_error_message)

    @pytest.mark.credentials
    def test_that_a_screenshot_can_be_added(self, mozwebqa, login_existing, free_app):
        """Test the happy path for adding a screenshot for a free submitted app."""

        edit_listing = self._go_to_edit_listing_page(mozwebqa, free_app)
        before_screenshots_count = len(edit_listing.screenshots_previews)

        # bring up the media form for the first free app
        media_region = edit_listing.click_edit_media()
        screenshots_count = len(media_region.screenshots)

        # upload a new screenshot
        media_region.screenshot_upload(self._get_resource_path('img.jpg'))

        # check that the screenshot list is updated
        new_screenshots_count = len(media_region.screenshots)
        Assert.equal(screenshots_count + 1, new_screenshots_count,
                     'Expected %s screenshots, but there are %s.' % (screenshots_count + 1, new_screenshots_count))

        # save the changes
        media_region.click_save_changes()

        # check that the icon preview has been updated
        after_screenshots_count = len(edit_listing.screenshots_previews)
        Assert.equal(before_screenshots_count + 1, len(edit_listing.screenshots_previews),
                     'Expected %s screenshots, but there are %s.' % (before_screenshots_count + 1, after_screenshots_count))

    @pytest.mark.credentials
    def test_that_a_screenshot_cannot_be_added_via_an_invalid_file_format(self, mozwebqa, login_existing, free_app):
        """Check that a tiff cannot be successfully uploaded as a screenshot."""

        edit_listing = self._go_to_edit_listing_page(mozwebqa, free_app)

        # bring up the media form for the first free app
        media_region = edit_listing.click_edit_media()

        # upload a new screenshot
        media_region.screenshot_upload(self._get_resource_path('img.tiff'))

        # check that the expected error message is displayed
        screenshot_upload_error_message = media_region.screenshot_upload_error_message
        Assert.contains('There was an error uploading your file.', screenshot_upload_error_message)
        Assert.contains('Images must be either PNG or JPG.', screenshot_upload_error_message)

    @pytest.mark.credentials
    def test_that_an_icon_cannot_be_added_via_an_invalid_file_format(self, mozwebqa, login_existing, free_app):
        """Check that a tiff cannot be successfully uploaded as an app icon."""

        edit_listing = self._go_to_edit_listing_page(mozwebqa, free_app)

        # bring up the media form for the first free app
        media_region = edit_listing.click_edit_media()

        # upload a new icon with an invalid format
        media_region.icon_upload(self._get_resource_path('img.tiff'))

        # check that the expected error message is displayed
        Assert.contains('Images must be either PNG or JPG.', media_region.icon_upload_error_message)

    @pytest.mark.nondestructive
    @pytest.mark.credentials
    def test_that_checks_apps_are_sorted_by_name(self, mozwebqa, login_existing):
        dev_home = Home(mozwebqa)
        dev_submissions = dev_home.header.click_my_submissions()
        dev_submissions.sorter.sort_by('Name')

        submitted_app_names = [app.name.lower() for app in dev_submissions.submitted_apps]
        Assert.is_sorted_ascending(submitted_app_names, 'Apps are not sorted ascending.\nApp names = %s' % submitted_app_names)

    @pytest.mark.nondestructive
    @pytest.mark.credentials
    def test_that_checks_apps_are_sorted_by_date(self, mozwebqa, login_existing):
        dev_home = Home(mozwebqa)
        dev_submissions = dev_home.header.click_my_submissions()
        dev_submissions.sorter.sort_by('Created')

        import time
        previous_app_date = time.gmtime()

        pages_to_test = 10 if dev_submissions.paginator.total_page_number >= 10 else dev_submissions.paginator.total_page_number
        for i in range(1, pages_to_test):
            for app in dev_submissions.submitted_apps:
                if app.has_date:
                    Assert.greater_equal(previous_app_date, app.date, 'Apps are not sorted ascending. According to Created date.')
                    previous_app_date = app.date
            dev_submissions.paginator.click_next_page()
