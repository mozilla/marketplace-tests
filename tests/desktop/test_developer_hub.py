#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


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

        '''Agree with the developer agreement and continue if it was not accepted
        in a previous app submit'''
        manifest_form = dev_agreement.click_continue()
        Assert.true(manifest_form.is_the_current_submission_stage, '\n Expected step is: App Manifest \n Actual step is: %s' % manifest_form.current_step)

        '''submit the app manifest url and validate it'''
        manifest_form.type_app_manifest_url(app['url'])
        manifest_form.click_validate()
        Assert.true(manifest_form.app_validation_status,
                    msg=manifest_form.app_validation_message)

        app_details = manifest_form.click_continue()
        Assert.true(app_details.is_the_current_submission_stage, '\n Expected step is: Details \n Actual step is: %s' % app_details.current_step)

        '''add custom app details for every field'''
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
            '''check/uncheck the checkbox according to the app value'''
            app_details.select_device_type(*device)

        for category in app['categories']:
            '''check/uncheck the checkbox according to the app value'''
            app_details.select_categories(*category)

        app_details.screenshot_upload(app['screenshot_link'])

        payments = app_details.click_continue()
        Assert.true(payments.is_the_current_submission_stage, '\n Expected step is: Payments \n Actual step is: %s' % payments.current_step)

        '''select the app payment method'''
        payments.select_payment_type(app['payment_type'])

        finished_form = payments.click_continue()
        Assert.true(finished_form.is_the_current_submission_stage, '\n Expected step is: Finished! \n Actual step is: %s' % finished_form.current_step)

        '''check that the app subission prcedure finished with succes'''
        Assert.equal('Success! What happens now?', finished_form.success_message)
