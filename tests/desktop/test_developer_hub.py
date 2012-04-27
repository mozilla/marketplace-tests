#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from unittestzero import Assert

from pages.desktop.developer_hub import DeveloperHub


class TestDeveloperHub:

    def test_app_submission(self, mozwebqa):
        dev_hub = DeveloperHub(mozwebqa)
        dev_hub.go_to_developer_hub()
        dev_hub.login()
        app = dev_hub.generate_test_app()

        dev_agreement = dev_hub.header.click_submit_app()

        #Agree with the developer agreement and continue if it was not accepted
        #in a previous app submit
        manifest_form = dev_agreement.click_continue()
        manifest_form.is_the_current_submission_stage

        #submit the app manifest url and validate it
        manifest_form.type_app_manifest_url(app['url'])
        manifest_form.click_validate()
        Assert.true(manifest_form.app_validation_status,
                    msg=manifest_form.app_validation_message)

        app_details = manifest_form.click_continue()
        app_details.is_the_current_submission_stage

        #add custom app details for every field
        app_details.click_change_name()
        app_details.type_name(app['name'])
        app_details.type_url_end(app['url_end'])
        app_details.type_summary(app['sumary'])
        app_details.type_descripion(app['description'])
        app_details.type_privacy_policy(app['privacy_policy'])
        app_details.type_homepage(app['homepage'])
        app_details.type_support_url(app['support_website'])
        app_details.type_support_email(app['support_email'])

        for dev in app['device_type']:
            if dev['value']:
                app_details.device_type[dev['name']].check()
            else:
                app_details.device_type[dev['name']].uncheck()

        for category in app['categories']:
            if category['value']:
                app_details.app_categories[category['name']].check()
            else:
                app_details.app_categories[category['name']].uncheck()

        app_details.screenshot_upload(app['screenshot_link'])

        payments = app_details.click_continue()
        payments.is_the_current_submission_stage

        #select the app payment method
        for pay_type in app['payment_type']:
            if pay_type['value']:
                payments.payment_type[pay_type['name']].check()

        finished_form = payments.click_continue()
        finished_form.is_the_current_submission_stage

        #check that the app subission prcedure finished with succes
        Assert.equal('Success! What happens now?', finished_form.success_message)
