#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest

from unittestzero import Assert

from pages.desktop.developer_hub import DeveloperHub
from mocks.mock_application import MockApplication


class TestDeveloperHub:

    def test_app_submission(self, mozwebqa):

        app = MockApplication()

        dev_hub = DeveloperHub(mozwebqa)
        dev_hub.go_to_developer_hub()
        dev_hub.login()

        dev_agreement = dev_hub.header.click_submit_app()

        """Agree with the developer agreement and continue if it was not accepted
        in a previous app submit"""
        manifest_form = dev_agreement.click_continue()
        Assert.true(manifest_form.is_the_current_submission_stage, '\n Expected step is: App Manifest \n Actual step is: %s' % manifest_form.current_step)

        """submit the app manifest url and validate it"""
        manifest_form.type_app_manifest_url(app['url'])
        manifest_form.click_validate()
        Assert.true(manifest_form.app_validation_status,
                    msg=manifest_form.app_validation_message)

        app_details = manifest_form.click_continue()
        Assert.true(app_details.is_the_current_submission_stage, '\n Expected step is: Details \n Actual step is: %s' % app_details.current_step)

        """add custom app details for every field"""
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
            """check/uncheck the checkbox according to the app value"""
            app_details.select_device_type(*device)

        for category in app['categories']:
            """check/uncheck the checkbox according to the app value"""
            app_details.select_categories(*category)

        app_details.screenshot_upload(app['screenshot_link'])

        payments = app_details.click_continue()
        Assert.true(payments.is_the_current_submission_stage, '\n Expected step is: Payments \n Actual step is: %s' % payments.current_step)

        """select the app payment method"""
        payments.select_payment_type(app['payment_type'])

        finished_form = payments.click_continue()
        Assert.true(finished_form.is_the_current_submission_stage, '\n Expected step is: Finished! \n Actual step is: %s' % finished_form.current_step)

        """check that the app submission procedure finished with success"""
        Assert.equal('Success! What happens now?', finished_form.success_message)

    @pytest.mark.nondestructive
    def test_that_checks_apps_are_sorted_by_name(self, mozwebqa):
        dev_hub = DeveloperHub(mozwebqa)
        dev_hub.go_to_developer_hub()
        dev_hub.login()

        dev_hub.sorter.sort_by('Name')

        submited_app_names = [app.name for app in dev_hub.submited_apps]
        Assert.is_sorted_ascending(submited_app_names, 'Apps are not sorted ascending.\nApp names = %s' % submited_app_names)

    @pytest.mark.nondestructive
    @pytest.mark.xfail(reason="Bugzilla 753287 Sorting by submitted apps by 'Created' mixes apps with submission process finished with apps with a incomplete status")
    def test_that_checks_apps_are_sorted_by_date(self, mozwebqa):
        dev_hub = DeveloperHub(mozwebqa)
        dev_hub.go_to_developer_hub()
        dev_hub.login()

        dev_hub.sorter.sort_by('Created')

        incomplete_apps = False
        import time
        previous_app_date = time.gmtime()

        while not dev_hub.paginator.is_next_page_disabled:
            for app in dev_hub.submited_apps:
                if app.is_incomplete:
                    incomplete_apps = True
                else:
                    if not incomplete_apps:
                        Assert.greater_equal(previous_app_date, app.date, 'Apps are not sorted ascending. According to Created date.')
                    else:
                        Assert.fail('Apps with a finished submission process are found after apps with the submission process unfinished')
            dev_hub.paginator.click_next_page()
