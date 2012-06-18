#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest
from selenium.common.exceptions import InvalidElementStateException
from unittestzero import Assert

from pages.desktop.developer_hub.home import Home
from mocks.mock_application import MockApplication


class TestDeveloperHub:

    def test_app_submission(self, mozwebqa):

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
        Assert.true(payments.is_the_current_submission_stage, '\n Expected step is: Payments \n Actual step is: %s' % payments.current_step)

        # select the app payment method
        payments.select_payment_type(app['payment_type'])

        finished_form = payments.click_continue()
        Assert.true(finished_form.is_the_current_submission_stage, '\n Expected step is: Finished! \n Actual step is: %s' % finished_form.current_step)

        # check that the app submission procedure finished with success
        Assert.equal('Success! What happens now?', finished_form.success_message)

    def _navigate_to_first_free_app(self, mozwebqa):
        """Navigate to the first free app submission."""
        dev_home = Home(mozwebqa)
        dev_home.go_to_developers_homepage()
        dev_home.login(user="default")
        my_apps = dev_home.header.click_my_apps()
        return my_apps.first_free_app

    def test_that_checks_editing_basic_info_for_a_free_app(self, mozwebqa):
        """Test the happy path for editing the basic information for a free submitted app.

        Pivotal link: https://www.pivotaltracker.com/projects/477093#!/stories/27741011
        Litmus link: https://litmus.mozilla.org/show_test.cgi?id=50478
        """
        updated_app = MockApplication()
        app_listing = self._navigate_to_first_free_app(mozwebqa)

        # update the details of the app
        basic_info = app_listing.click_edit_basic_info()
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
        Assert.true(updated_app['url_end'] in app_listing.url_end)
        Assert.equal(app_listing.summary, updated_app['summary'])
        Assert.equal(app_listing.categories.sort(), updated_app['categories'].sort())
        Assert.equal(app_listing.device_types.sort(), updated_app['device_type'].sort())

    @pytest.mark.nondestructive
    def test_that_checks_that_manifest_url_cannot_be_edited_via_basic_info_for_a_free_app(self, mozwebqa):
        """Ensure that the manifest url cannot be edited via the basic info form.

        Pivotal link: https://www.pivotaltracker.com/projects/477093#!/stories/27741011
        Litmus link: https://litmus.mozilla.org/show_test.cgi?id=50478
        """
        with pytest.raises(InvalidElementStateException):
            app_listing = self._navigate_to_first_free_app(mozwebqa)
            basic_info = app_listing.click_edit_basic_info()
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

        Pivotal link: https://www.pivotaltracker.com/projects/477093#!/stories/27741011
        Litmus link: https://litmus.mozilla.org/show_test.cgi?id=50478
        """
        app_listing = self._navigate_to_first_free_app(mozwebqa)
        basic_info = app_listing.click_edit_basic_info()
        basic_info.type_summary('1234567890' * 26)
        Assert.false(basic_info.is_summary_char_count_ok, 'The character count for summary should display as an error but it does not')
        basic_info.click_save_changes()
        Assert.true('Ensure this value has at most 250 characters' in basic_info.summary_char_count_error_message)
        Assert.true(basic_info.is_this_form_open)

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
