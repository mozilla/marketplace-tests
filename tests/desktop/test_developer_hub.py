#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest
from selenium.common.exceptions import InvalidElementStateException
from unittestzero import Assert

from mocks.mock_application import MockApplication
from pages.desktop.developer_hub.home import Home
from tests.base_test import BaseTest
from pages.desktop.paypal.paypal import PayPal


class TestDeveloperHub(BaseTest):

    def test_free_app_submission(self, mozwebqa):

        app = MockApplication()

        dev_home = Home(mozwebqa)
        dev_home.go_to_developers_homepage()
        dev_home.login(user="default")

        dev_agreement = dev_home.header.click_submit_app()

        """Agree with the developer agreement and continue if it was not accepted
        in a previous app submit"""
        manifest_form = dev_agreement.click_continue()
        Assert.true(manifest_form.is_the_current_submission_stage, '\n Expected step is: App Manifest \n Actual step is: %s' % manifest_form.current_step)

        # submit the app manifest url and validate it
        manifest_form.type_app_manifest_url(app['url'])
        manifest_form.click_validate()
        Assert.true(manifest_form.app_validation_status,
                    msg=manifest_form.app_validation_message)

        app_details = manifest_form.click_continue()
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

        payments = app_details.click_continue()
        Assert.true(payments.is_the_current_submission_stage, '\n Expected step is: Payments \n Actual step is: %s' % payments.current_step)

        # select the app payment method
        payments.select_payment_type(app['payment_type'])

        finished_form = payments.click_continue()
        Assert.true(finished_form.is_the_current_submission_stage, '\n Expected step is: Finished! \n Actual step is: %s' % finished_form.current_step)

        # check that the app submission procedure succeeded
        Assert.equal('Success! What happens now?', finished_form.success_message)

    def test_premium_app_submission(self, mozwebqa):

        developer_paypal_page = PayPal(mozwebqa)
        developer_paypal_page.go_to_page()
        developer_paypal_page.login_paypal(user="paypal")
        Assert.true(developer_paypal_page.is_user_logged_in)

        app = MockApplication(payment_type='Premium')

        dev_home = Home(mozwebqa)
        dev_home.go_to_developers_homepage()
        dev_home.login(user="default")

        dev_agreement = dev_home.header.click_submit_app()

        """Agree with the developer agreement and continue if it was not accepted
        in a previous app submit"""
        manifest_form = dev_agreement.click_continue()
        Assert.true(manifest_form.is_the_current_submission_stage,
                    '\n Expected step is: App Manifest \n Actual step is: %s' % manifest_form.current_step)

        # submit the app manifest url and validate it
        manifest_form.type_app_manifest_url(app['url'])
        manifest_form.click_validate()
        Assert.true(manifest_form.app_validation_status,
                    msg=manifest_form.app_validation_message)

        app_details = manifest_form.click_continue()
        Assert.true(app_details.is_the_current_submission_stage, '\n Expected step is: Details \n Actual step is: %s' % app_details.current_step)

        # add custom app details for every field
        app_details.click_change_name()
        app_details.type_name(app['name'])
        app_details.type_url_end(app['url_end'])
        app_details.type_summary(app['summary'])
        app_details.type_descripion(app['description'])
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

        payments = app_details.click_continue()

        # select the app payment method
        payments.select_payment_type(app['payment_type'])

        up_sell = payments.click_continue()

        up_sell.select_price(app['app_price'])
        up_sell.make_public(app['make_public'])

        pay_pal = up_sell.click_continue()

        pay_pal.select_paypal_account(app['business_account'])
        pay_pal.paypal_email(mozwebqa.credentials['sandbox']['email'])

        bounce = pay_pal.click_continue()

        paypall_sandbox = bounce.click_setup_permissions()

        paypall_sandbox.login_paypal_sandbox()
        contact_information = paypall_sandbox.click_grant_permission()

        contact_information.first_name(app['first_name'])
        contact_information.last_name(app['last_name'])
        contact_information.address_field_one(app['address'])
        contact_information.city(app['city'])
        contact_information.state(app['state'])
        contact_information.post_code(app['post_code'])
        contact_information.country(app['country'])
        contact_information.phone(app['phone'])

        finished_form = contact_information.click_continue()
        Assert.true(finished_form.is_the_current_submission_stage, '\n Expected step is: Finished! \n Actual step is: %s' % finished_form.current_step)

        # check that the app submission procedure finished with success
        Assert.equal('Success! What happens now?', finished_form.success_message)

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
        my_apps = dev_home.header.click_my_apps()

        # bring up the basic info form for the first free app
        basic_info = my_apps.first_free_app.click_edit_basic_info()

        # update the details of the app
        basic_info.type_name(updated_app['name'])
        basic_info.type_url_end(updated_app['url_end'])
        basic_info.type_summary(updated_app['summary'])

        for device in updated_app['device_type']:
            # check/uncheck the checkbox according to the app value
            basic_info.select_device_type(*device)

        for category in updated_app['categories']:
            # check/uncheck the checkbox according to the app value
            basic_info.select_categories(*category)

        app_listing = basic_info.click_save_changes()

        # check that the listing has been updated
        Assert.true(app_listing.no_forms_are_open)
        Assert.equal(app_listing.name, updated_app['name'])
        Assert.contains(updated_app['url_end'], app_listing.url_end)
        Assert.equal(app_listing.summary, updated_app['summary'])
        Assert.equal(app_listing.categories.sort(), updated_app['categories'].sort())
        Assert.equal(app_listing.device_types.sort(), updated_app['device_type'].sort())

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
        my_apps = dev_home.header.click_my_apps()

        # update fields in support information
        support_info = my_apps.first_free_app.click_support_information()
        support_info.type_support_email([updated_app['support_email']])
        support_info.type_support_url([updated_app['support_website']])

        app_listing = support_info.click_save_changes()

        # Verify the changes have been made
        Assert.equal(app_listing.email, updated_app['support_email'])
        Assert.equal(app_listing.website, updated_app['support_website'])

    @pytest.mark.nondestructive
    def test_that_checks_that_manifest_url_cannot_be_edited_via_basic_info_for_a_free_app(self, mozwebqa):
        """Ensure that the manifest url cannot be edited via the basic info form.

        Litmus link: https://litmus.mozilla.org/show_test.cgi?id=50478
        """
        with pytest.raises(InvalidElementStateException):
            dev_home = Home(mozwebqa)
            dev_home.go_to_developers_homepage()
            dev_home.login(user="default")
            my_apps = dev_home.header.click_my_apps()

            # bring up the basic info form for the first free app
            basic_info = my_apps.first_free_app.click_edit_basic_info()
            """attempting to type into the manifest_url input should raise an
            InvalidElementStateException"""
            basic_info.type_manifest_url('any value should cause an exception')

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
        my_apps = dev_home.header.click_my_apps()

        # bring up the basic info form for the first free app
        basic_info = my_apps.first_free_app.click_edit_basic_info()
        basic_info.type_summary('1234567890' * 26)
        Assert.false(basic_info.is_summary_char_count_ok,
            'The character count for summary should display as an error but it does not')
        basic_info = basic_info.click_save_changes('failure')
        Assert.contains('Ensure this value has at most 250 characters',
                    basic_info.summary_error_message)
        Assert.true(basic_info.is_this_form_open)

    def test_that_checks_required_field_validations_on_basic_info_for_a_free_app(self, mozwebqa):
        """Ensure that all required fields generate warning messages and prevent form submission.

        Litmus link: https://litmus.mozilla.org/show_test.cgi?id=50478
        """
        dev_home = Home(mozwebqa)
        dev_home.go_to_developers_homepage()
        dev_home.login(user="default")
        my_apps = dev_home.header.click_my_apps()

        # bring up the basic info form for the first free app
        basic_info = my_apps.first_free_app.click_edit_basic_info()

        # check name validation
        basic_info.type_name('')
        basic_info = basic_info.click_save_changes('failure')
        Assert.true(basic_info.is_this_form_open)
        Assert.contains('This field is required.', basic_info.name_error_message)
        basic_info.type_name('something')

        # check App URL validation
        basic_info.type_url_end('')
        basic_info = basic_info.click_save_changes('failure')
        Assert.true(basic_info.is_this_form_open)
        Assert.contains('This field is required.', basic_info.url_end_error_message)
        basic_info.type_url_end('something')

        # check Summary validation
        basic_info.type_summary('')
        basic_info = basic_info.click_save_changes('failure')
        Assert.true(basic_info.is_this_form_open)
        Assert.contains('This field is required.', basic_info.summary_error_message)
        basic_info.type_summary('something')

        # check Categories validation
        basic_info.clear_categories()
        basic_info = basic_info.click_save_changes('failure')
        Assert.true(basic_info.is_this_form_open)
        Assert.contains('This field is required.', basic_info.categories_error_message)
        basic_info.select_categories('Music', True)

        # check Device Types
        basic_info.clear_device_types()
        basic_info = basic_info.click_save_changes('failure')
        Assert.true(basic_info.is_this_form_open)
        Assert.contains('This field is required.', basic_info.device_types_error_message)

    def test_that_app_icon_can_be_updated(self, mozwebqa):
        """Test the happy path for editing the app icon for a free submitted app.

        Litmus link: https://litmus.mozilla.org/show_test.cgi?id=50479
        """
        dev_home = Home(mozwebqa)
        dev_home.go_to_developers_homepage()
        dev_home.login(user="default")
        my_apps = dev_home.header.click_my_apps()
        app_listing = my_apps.first_free_app
        before_icon_src = app_listing.icon_preview_src

        # bring up the media form for the first free app
        media = app_listing.click_edit_media()
        icon_64_src = media.icon_preview_64_image_src
        icon_32_src = media.icon_preview_32_image_src

        # upload a new icon
        media.icon_upload(self._get_resource_path('img.jpg'))

        # check that the preview is updated
        Assert.not_equal(icon_64_src, media.icon_preview_64_image_src,
            'The 64x64 icon should have changed, but it did not.')
        Assert.not_equal(icon_32_src, media.icon_preview_32_image_src,
            'The 32x32 icon should have changed, but it did not.')

        # save the changes
        app_listing = media.click_save_changes()

        # check that the icon preview has been updated
        Assert.not_equal(before_icon_src, app_listing.icon_preview_src,
            'The app icon preview should have changed, but it did not.')

    def test_that_cancelling_an_app_icon_update_does_not_update_the_icon(self, mozwebqa):
        """Upload a new app icon, then cancel and ensure that the new icon is not used.

        Litmus link: https://litmus.mozilla.org/show_test.cgi?id=50479
        """
        dev_home = Home(mozwebqa)
        dev_home.go_to_developers_homepage()
        dev_home.login(user="default")
        my_apps = dev_home.header.click_my_apps()
        app_listing = my_apps.first_free_app
        before_icon_src = app_listing.icon_preview_src

        # bring up the media form for the first free app
        media = app_listing.click_edit_media()
        icon_64_src = media.icon_preview_64_image_src
        icon_32_src = media.icon_preview_32_image_src

        # upload a new icon
        media.icon_upload(self._get_resource_path('img.jpg'))

        # check that the preview is updated
        Assert.not_equal(icon_64_src, media.icon_preview_64_image_src,
            'The 64x64 icon should have changed, but it did not.')
        Assert.not_equal(icon_32_src, media.icon_preview_32_image_src,
            'The 32x32 icon should have changed, but it did not.')

        # cancel the changes
        app_listing = media.click_cancel()

        # check that the icon preview has been updated
        Assert.equal(before_icon_src, app_listing.icon_preview_src,
            'The app icon preview should not have changed, but it did.')

    def test_that_a_screenshot_can_be_added(self, mozwebqa):
        """Test the happy path for adding a screenshot for a free submitted app.

        Litmus link: https://litmus.mozilla.org/show_test.cgi?id=50479
        """
        dev_home = Home(mozwebqa)
        dev_home.go_to_developers_homepage()
        dev_home.login(user="default")
        my_apps = dev_home.header.click_my_apps()
        app_listing = my_apps.first_free_app
        before_screenshots_count = len(app_listing.screenshots_previews)

        # bring up the media form for the first free app
        media = app_listing.click_edit_media()
        screenshots_count = len(media.screenshots)

        # upload a new screenshot
        media.screenshot_upload(self._get_resource_path('img.jpg'))

        # check that the screenshot list is updated
        new_screenshots_count = len(media.screenshots)
        Assert.equal(screenshots_count + 1, new_screenshots_count,
            'Expected %s screenshots, but there are %s.' % (screenshots_count + 1, new_screenshots_count))

        # save the changes
        app_listing = media.click_save_changes()

        # check that the icon preview has been updated
        after_screenshots_count = len(app_listing.screenshots_previews)
        Assert.equal(before_screenshots_count + 1, len(app_listing.screenshots_previews),
            'Expected %s screenshots, but there are %s.' % (before_screenshots_count + 1, after_screenshots_count))

    def test_that_a_screenshot_cannot_be_added_via_an_invalid_file_format(self, mozwebqa):
        """Check that a tiff cannot be successfully uploaded as a screenshot..

        Litmus link: https://litmus.mozilla.org/show_test.cgi?id=50479
        """
        dev_home = Home(mozwebqa)
        dev_home.go_to_developers_homepage()
        dev_home.login(user="default")
        my_apps = dev_home.header.click_my_apps()
        app_listing = my_apps.first_free_app

        # bring up the media form for the first free app
        media = app_listing.click_edit_media()

        # upload a new screenshot
        media.screenshot_upload(self._get_resource_path('img.tiff'))

        # check that the expected error message is displayed
        screenshot_upload_error_message = media.screenshot_upload_error_message
        Assert.contains('There was an error uploading your file.', screenshot_upload_error_message)
        Assert.contains('Images must be either PNG or JPG.', screenshot_upload_error_message)

    def test_that_an_icon_cannot_be_added_via_an_invalid_file_format(self, mozwebqa):
        """Check that a tiff cannot be successfully uploaded as an app icon.

        Litmus link: https://litmus.mozilla.org/show_test.cgi?id=50479
        """
        dev_home = Home(mozwebqa)
        dev_home.go_to_developers_homepage()
        dev_home.login(user="default")
        my_apps = dev_home.header.click_my_apps()
        app_listing = my_apps.first_free_app

        # bring up the media form for the first free app
        media = app_listing.click_edit_media()

        # upload a new icon with an invalid format
        media.icon_upload(self._get_resource_path('img.tiff'))

        # check that the expected error message is displayed
        Assert.contains('Images must be either PNG or JPG.',media.icon_upload_error_message)

    @pytest.mark.nondestructive
    def test_that_checks_apps_are_sorted_by_name(self, mozwebqa):
        dev_home = Home(mozwebqa)
        dev_home.go_to_developers_homepage()
        dev_home.login(user="default")

        dev_submissions = dev_home.header.click_my_apps()
        dev_submissions.sorter.sort_by('Name')

        submitted_app_names = [app.name for app in dev_submissions.submitted_apps]
        Assert.is_sorted_ascending(submitted_app_names, 'Apps are not sorted ascending.\nApp names = %s' % submitted_app_names)

    @pytest.mark.nondestructive
    @pytest.mark.xfail(reason="Bugzilla 753287 Sorting by submitted apps by 'Created' mixes apps with submission process finished with apps with a incomplete status")
    def test_that_checks_apps_are_sorted_by_date(self, mozwebqa):
        dev_home = Home(mozwebqa)
        dev_home.go_to_developers_homepage()
        dev_home.login(user="default")

        dev_submissions = dev_home.header.click_my_apps()

        dev_submissions.sorter.sort_by('Created')

        incomplete_apps = False
        import time
        previous_app_date = time.gmtime()

        while not dev_submissions.paginator.is_next_page_disabled:
            for app in dev_submissions.submitted_apps:
                if app.is_incomplete:
                    incomplete_apps = True
                else:
                    if not incomplete_apps:
                        Assert.greater_equal(previous_app_date, app.date, 'Apps are not sorted ascending. According to Created date.')
                    else:
                        Assert.fail('Apps with a finished submission process are found after apps with the submission process unfinished')
            dev_submissions.paginator.click_next_page()
