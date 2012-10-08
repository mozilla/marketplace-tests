#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest
from selenium.common.exceptions import InvalidElementStateException
from unittestzero import Assert

from mocks.mock_application import MockApplication
from pages.desktop.developer_hub.home import Home
from tests.desktop.base_test import BaseTest
from pages.desktop.paypal.paypal import PayPal


class TestDeveloperHub(BaseTest):

    @pytest.mark.xfail(reason="Bug 779740 - "Description already exists" error is displayed on the Additional Information field when submitting a new app")
    def test_hosted_app_submission(self, mozwebqa):

        app = MockApplication()

        dev_home = Home(mozwebqa)
        dev_home.go_to_developers_homepage()
        dev_home.login(user="default")

        dev_agreement = dev_home.click_submit_app()

        """Agree with the developer agreement and continue if it was not accepted
        in a previous app submit"""
        app_type = dev_agreement.click_continue()
        Assert.true(app_type.is_the_current_submission_stage, '\n Expected step is: App Manifest \n Actual step is: %s' % app_type.current_step)

        #select host it yourself app
        manifest_validation_form = app_type.click_host_it_yourself_app()

        # submit the app manifest url and validate it
        manifest_validation_form.type_app_manifest_url(app['url'])
        manifest_validation_form.click_validate()
        Assert.true(manifest_validation_form.app_validation_status,
                    msg=manifest_validation_form.app_validation_message)

        app_details = manifest_validation_form.click_continue()
        Assert.true(app_details.is_the_current_submission_stage, '\n Expected step is: Details \n Actual step is: %s' % app_details.current_step)

        # add custom app details for every field
        app_details.click_change_name()
        app_details.type_name(app['name'])
        app_details.type_url_end(app['url_end'])
        app_details.type_summary(app['summary'])
        app_details.type_description(app['description'])
        app_details.type_privacy_policy(app['privacy_policy'])
        app_details.type_homepage(app['homepage'])
        app_details.type_support_url(app['support_website'])
        app_details.type_support_email(app['support_email'])

        for device in app['device_type']:
            # check/uncheck the checkbox according to the app value
            app_details.select_device_type(*device)

        for category in app['categories']:
            # check/uncheck the checkbox according to the app value
            app_details.select_categories(*category)

        app_details.screenshot_upload(app['screenshot_link'])

        finished_form = app_details.click_continue()

        Assert.true(finished_form.is_the_current_submission_stage, '\n Expected step is: Finished! \n Actual step is: %s' % finished_form.current_step)

        # check that the app submission procedure succeeded
        Assert.equal('Success! What happens now?', finished_form.success_message)

    def test_that_deletes_app(self, mozwebqa):
        dev_home = Home(mozwebqa)
        dev_home.go_to_developers_homepage()
        dev_home.login(user="default")

        my_apps = dev_home.header.click_my_submissions()

        first_free_app = my_apps.first_free_app
        app_name = first_free_app.name

        self._delete_app(mozwebqa, app_name)

        Assert.true(my_apps.is_notification_visibile)
        Assert.true(my_apps.is_notification_succesful, my_apps.notification_message)
        Assert.equal("App deleted.", my_apps.notification_message)

        for i in range(1, my_apps.paginator.total_page_number + 1):
            for app in my_apps.submitted_apps:
                Assert.not_equal(app.name, app_name)
            if my_apps.paginator.is_paginator_present:
                if not my_apps.paginator.is_first_page_disabled:
                    my_apps.paginator.click_next_page()

    def test_that_checks_editing_basic_info_for_a_free_app(self, mozwebqa):
        """Test the happy path for editing the basic information for a free submitted app.

        Litmus link: https://litmus.mozilla.org/show_test.cgi?id=50478
        """
        updated_app = MockApplication(
            categories = [('Entertainment', False), ('Games', True), ('Music', True)],
            device_type = [('Desktop', True), ('Mobile', True), ('Tablet', True)]
        )
        dev_home = Home(mozwebqa)
        dev_home.go_to_developers_homepage()
        dev_home.login(user="default")
        my_apps = dev_home.header.click_my_submissions()
        edit_listing = my_apps.first_free_app.click_edit()

        # bring up the basic info form for the first free app
        basic_info_region = edit_listing.click_edit_basic_info()

        # update the details of the app
        basic_info_region.type_name(updated_app['name'])
        basic_info_region.type_url_end(updated_app['url_end'])
        basic_info_region.type_summary(updated_app['summary'])

        for device in updated_app['device_type']:
            # check/uncheck the checkbox according to the app value
            basic_info_region.select_device_type(*device)

        for category in updated_app['categories']:
            # check/uncheck the checkbox according to the app value
            basic_info_region.select_categories(*category)

        basic_info_region.click_save_changes()

        # check that the listing has been updated
        Assert.true(edit_listing.no_forms_are_open)
        Assert.equal(edit_listing.name, updated_app['name'])
        Assert.contains(updated_app['url_end'], edit_listing.url_end)
        Assert.equal(edit_listing.summary, updated_app['summary'])
        Assert.equal(edit_listing.categories.sort(), updated_app['categories'].sort())
        Assert.equal(edit_listing.device_types.sort(), updated_app['device_type'].sort())

    @pytest.mark.xfail(reason="Bug 796864 Free app Edit Listing Edit Support Informations Edit email validation always returns Enter a valid e-mail address")
    def test_that_checks_editing_support_information_for_a_free_app(self, mozwebqa):
        """
        Test edit support information for a free app.

        Pivotal task: https://www.pivotaltracker.com/story/show/27741207
        Litmus: https://litmus.mozilla.org/show_test.cgi?id=50481
        """
        updated_app = MockApplication()

        dev_home = Home(mozwebqa)
        dev_home.go_to_developers_homepage()
        dev_home.login(user="default")
        my_apps = dev_home.header.click_my_submissions()
        edit_listing = my_apps.first_free_app.click_edit()

        # update fields in support information
        support_info_region = edit_listing.click_support_information()
        support_info_region.type_support_email(updated_app['support_email'])
        support_info_region.type_support_url(updated_app['support_website'])

        support_info_region.click_save_changes()

        # Verify the changes have been made
        Assert.equal(edit_listing.email, updated_app['support_email'])
        Assert.equal(edit_listing.website, updated_app['support_website'])

    @pytest.mark.nondestructive
    def test_that_checks_that_manifest_url_cannot_be_edited_via_basic_info_for_a_free_app(self, mozwebqa):
        """Ensure that the manifest url cannot be edited via the basic info form.

        Litmus link: https://litmus.mozilla.org/show_test.cgi?id=50478
        """
        with pytest.raises(InvalidElementStateException):
            dev_home = Home(mozwebqa)
            dev_home.go_to_developers_homepage()
            dev_home.login(user="default")
            my_apps = dev_home.header.click_my_submissions()

            # bring up the basic info form for the first free app
            edit_listing = my_apps.first_free_app.click_edit()
            basic_info_region = edit_listing.click_edit_basic_info()
            """attempting to type into the manifest_url input should raise an
            InvalidElementStateException"""
            basic_info_region.type_manifest_url('any value should cause an exception')

    def test_that_checks_that_summary_must_be_limited_to_250_chars_on_basic_info_for_a_free_app(self, mozwebqa):
        """Ensure that the summary field cannot contain over 250 characters.

        Tests:
        - the message showing the number of characters remaining appears with an error class
        if the limit is exceeded
        - after submission with the limit exceeded an error message is displayed
        - the form cannot be successfully submitted if the limit is exceeded

        Litmus link: https://litmus.mozilla.org/show_test.cgi?id=50478
        """
        dev_home = Home(mozwebqa)
        dev_home.go_to_developers_homepage()
        dev_home.login(user="default")
        my_apps = dev_home.header.click_my_submissions()

        # bring up the basic info form for the first free app
        edit_listing = my_apps.first_free_app.click_edit()
        basic_info_region = edit_listing.click_edit_basic_info()
        basic_info_region.type_summary('1234567890' * 26)
        Assert.false(basic_info_region.is_summary_char_count_ok,
            'The character count for summary should display as an error but it does not')
        basic_info_region.click_save_changes()
        Assert.contains('Ensure this value has at most 250 characters',
                    basic_info_region.summary_error_message)
        Assert.true(basic_info_region.is_this_form_open)

    def test_that_checks_required_field_validations_on_basic_info_for_a_free_app(self, mozwebqa):
        """Ensure that all required fields generate warning messages and prevent form submission.

        Litmus link: https://litmus.mozilla.org/show_test.cgi?id=50478
        """
        dev_home = Home(mozwebqa)
        dev_home.go_to_developers_homepage()
        dev_home.login(user="default")
        my_apps = dev_home.header.click_my_submissions()

        # bring up the basic info form for the first free app
        edit_listing = my_apps.first_free_app.click_edit()
        basic_info_region = edit_listing.click_edit_basic_info()

        # check name validation
        basic_info_region.type_name('')
        basic_info_region.click_save_changes()
        Assert.true(basic_info_region.is_this_form_open)
        Assert.contains('This field is required.', basic_info_region.name_error_message)
        basic_info_region.type_name('something')

        # check App URL validation
        basic_info_region.type_url_end('')
        basic_info_region.click_save_changes()
        Assert.true(basic_info_region.is_this_form_open)
        Assert.contains('This field is required.', basic_info_region.url_end_error_message)
        basic_info_region.type_url_end('something')

        # check Summary validation
        basic_info_region.type_summary('')
        basic_info_region.click_save_changes()
        Assert.true(basic_info_region.is_this_form_open)
        Assert.contains('This field is required.', basic_info_region.summary_error_message)
        basic_info_region.type_summary('something')

        # check Categories validation
        basic_info_region.clear_categories()
        basic_info_region.click_save_changes()
        Assert.true(basic_info_region.is_this_form_open)
        Assert.contains('This field is required.', basic_info_region.categories_error_message)
        basic_info_region.select_categories('Music', True)

        # check Device Types
        basic_info_region.clear_device_types()
        basic_info_region.click_save_changes()
        Assert.true(basic_info_region.is_this_form_open)
        Assert.contains('This field is required.', basic_info_region.device_types_error_message)

    def test_that_a_screenshot_can_be_added(self, mozwebqa):
        """Test the happy path for adding a screenshot for a free submitted app.

        Litmus link: https://litmus.mozilla.org/show_test.cgi?id=50479
        """
        dev_home = Home(mozwebqa)
        dev_home.go_to_developers_homepage()
        dev_home.login(user="default")
        my_apps = dev_home.header.click_my_submissions()
        edit_listing = my_apps.first_free_app.click_edit()
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

    def test_that_a_screenshot_cannot_be_added_via_an_invalid_file_format(self, mozwebqa):
        """Check that a tiff cannot be successfully uploaded as a screenshot..

        Litmus link: https://litmus.mozilla.org/show_test.cgi?id=50479
        """
        dev_home = Home(mozwebqa)
        dev_home.go_to_developers_homepage()
        dev_home.login(user="default")
        my_apps = dev_home.header.click_my_submissions()
        edit_listing = my_apps.first_free_app.click_edit()

        # bring up the media form for the first free app
        media_region = edit_listing.click_edit_media()

        # upload a new screenshot
        media_region.screenshot_upload(self._get_resource_path('img.tiff'))

        # check that the expected error message is displayed
        screenshot_upload_error_message = media_region.screenshot_upload_error_message
        Assert.contains('There was an error uploading your file.', screenshot_upload_error_message)
        Assert.contains('Images must be either PNG or JPG.', screenshot_upload_error_message)

    def test_that_an_icon_cannot_be_added_via_an_invalid_file_format(self, mozwebqa):
        """Check that a tiff cannot be successfully uploaded as an app icon.

        Litmus link: https://litmus.mozilla.org/show_test.cgi?id=50479
        """
        dev_home = Home(mozwebqa)
        dev_home.go_to_developers_homepage()
        dev_home.login(user="default")
        my_apps = dev_home.header.click_my_submissions()
        edit_listing = my_apps.first_free_app.click_edit()

        # bring up the media form for the first free app
        media_region = edit_listing.click_edit_media()

        # upload a new icon with an invalid format
        media_region.icon_upload(self._get_resource_path('img.tiff'))

        # check that the expected error message is displayed
        Assert.contains('Images must be either PNG or JPG.',media_region.icon_upload_error_message)

    @pytest.mark.nondestructive
    def test_that_checks_apps_are_sorted_by_name(self, mozwebqa):
        dev_home = Home(mozwebqa)
        dev_home.go_to_developers_homepage()
        dev_home.login(user="default")

        dev_submissions = dev_home.header.click_my_submissions()
        dev_submissions.sorter.sort_by('Name')

        submitted_app_names = [app.name for app in dev_submissions.submitted_apps]
        Assert.is_sorted_ascending(submitted_app_names, 'Apps are not sorted ascending.\nApp names = %s' % submitted_app_names)

    @pytest.mark.nondestructive
    @pytest.mark.xfail(reason="Bugzilla 753287 Sorting by submitted apps by 'Created' mixes apps with submission process finished with apps with a incomplete status")
    def test_that_checks_apps_are_sorted_by_date(self, mozwebqa):
        dev_home = Home(mozwebqa)
        dev_home.go_to_developers_homepage()
        dev_home.login(user="default")

        dev_submissions = dev_home.header.click_my_submissions()

        dev_submissions.sorter.sort_by('Created')

        incomplete_apps = False
        import time
        previous_app_date = time.gmtime()

        for i in range(1, dev_submissions.paginator.total_page_number):
            for app in dev_submissions.submitted_apps:
                if app.is_incomplete:
                    incomplete_apps = True
                else:
                    if not incomplete_apps:
                        Assert.greater_equal(previous_app_date, app.date, 'Apps are not sorted ascending. According to Created date.')
                    else:
                        Assert.fail('Apps with a finished submission process are found after apps with the submission process unfinished')
            dev_submissions.paginator.click_next_page()
