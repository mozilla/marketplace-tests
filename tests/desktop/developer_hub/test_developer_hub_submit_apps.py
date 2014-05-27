#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from unittestzero import Assert

from mocks.marketplace_api import MarketplaceAPI
from mocks.mock_application import MockApplication
from pages.desktop.developer_hub.home import Home
from tests.desktop.base_test import BaseTest


class TestDeveloperHubSubmitApps(BaseTest):

    @pytest.mark.credentials
    def test_packaged_app_submission(self, mozwebqa_devhub_logged_in):
        if '-dev.allizom' in mozwebqa_devhub_logged_in.base_url:
            env = 'dev'
        else:
            env = 'stage'

        app = MockApplication(env, app_type='packaged')

        dev_home = Home(mozwebqa_devhub_logged_in)

        dev_agreement = dev_home.click_submit_new_app()

        """Agree with the developer agreement and continue if it was not accepted
        in a previous app submit"""
        manifest_validation_form = dev_agreement.click_continue()

        # select device type
        for device in app['device_type']:
            if device[1]:
                manifest_validation_form.device_type(device[0])

        # select app type
        manifest_validation_form.app_type(app['app_type'])

        # submit the hosted app and validate it
        manifest_validation_form.upload_file(app['app_path'])
        manifest_validation_form.wait_for_app_validation()

        Assert.true(manifest_validation_form.app_validation_status,
                    msg=manifest_validation_form.app_validation_message)
        app_details = manifest_validation_form.click_continue()
        Assert.true(app_details.is_the_current_submission_stage, '\n Expected step is: Details \n Actual step is: %s' % app_details.current_step)

        # add custom app details for every field
        app_details.click_change_name()

        app_details.type_url_end(app['url_end'])
        app_details.type_description(app['description'])
        app_details.type_privacy_policy(app['privacy_policy'])
        app_details.type_homepage(app['homepage'])
        app_details.type_support_url(app['support_website'])
        app_details.type_support_email(app['support_email'])

        for category in app['categories']:
            # check/uncheck the checkbox according to the app value
            app_details.select_categories(*category)

        app_details.screenshot_upload(app['screenshot_link'])

        try:
            next_steps = app_details.click_continue()
            Assert.equal('Almost There!', next_steps.almost_there_message)

            content_ratings = next_steps.click_continue()
            Assert.equal('Get My App Rated', content_ratings.get_app_rated_message)

            # insert Submission ID and Security code to get app rated
            content_ratings.fill_in_app_already_rated_info(app['submission_id'], app['security_code'])
            content_ratings.click_submit()
            Assert.equal('Congratulations, your app submission is now complete and will be reviewed shortly!',
                         content_ratings.saved_ratings_message)
        except Exception as exception:
            Assert.fail(exception)
        finally:
            # Clean up app
            edit_app = dev_home.go_to_app_status_page(app)
            delete_popup = edit_app.click_delete_app()
            delete_popup.delete_app()

    @pytest.mark.credentials
    def test_hosted_paid_app_submission(self, mozwebqa_devhub_logged_in):
        if '-dev.allizom' in mozwebqa_devhub_logged_in.base_url:
            env = 'dev'
        else:
            env = 'stage'

        app = MockApplication(env)

        dev_home = Home(mozwebqa_devhub_logged_in)

        dev_agreement = dev_home.click_submit_new_app()

        """Agree with the developer agreement and continue if it was not accepted
        in a previous app submit"""
        manifest_validation_form = dev_agreement.click_continue()

        # select a premium
        manifest_validation_form.premium_type('paid')

        # select device type
        for device in app['device_type']:
            if device[1]:
                manifest_validation_form.device_type(device[0], 'paid')

        # submit the app manifest url and validate it
        manifest_validation_form.type_app_manifest_url(app['url'])
        manifest_validation_form.click_validate()
        Assert.true(manifest_validation_form.app_validation_status,
                    msg=manifest_validation_form.app_validation_message)

        app_details = manifest_validation_form.click_continue()
        Assert.true(app_details.is_the_current_submission_stage, '\n Expected step is: Details \n Actual step is: %s' % app_details.current_step)

        # add custom app details for every field
        app_details.click_change_name()
        app_details.type_url_end(app['url_end'])
        app_details.type_description(app['description'])
        app_details.type_privacy_policy(app['privacy_policy'])
        app_details.type_homepage(app['homepage'])
        app_details.type_support_url(app['support_website'])
        app_details.type_support_email(app['support_email'])

        for category in app['categories']:
            # check/uncheck the checkbox according to the app value
            app_details.select_categories(*category)

        app_details.screenshot_upload(app['screenshot_link'])
        try:
            next_steps = app_details.click_continue()
            Assert.equal('Almost There!', next_steps.almost_there_message)

            content_ratings = next_steps.click_continue()
            Assert.equal('Get My App Rated', content_ratings.get_app_rated_message)

            # insert Submission ID and Security code to get app rated
            content_ratings.fill_in_app_already_rated_info(app['submission_id'], app['security_code'])
            content_ratings.click_submit()
            Assert.equal('Content ratings successfully saved.',
                         content_ratings.saved_ratings_message)

            # setup payments
            payments = content_ratings.click_setup_payments()

            # select payment account
            payments.select_payment_account()

            # setup price tier
            app_price = '$0.10'
            payments.select_price(app_price)

            payments.click_payments_save_changes()
            Assert.true(payments.is_update_notification_visible)
            Assert.equal(payments.app_price, app_price, '\n Expected price is: %s \n Actual price is: %s' % (app_price, payments.app_price))

        except Exception as exception:
            Assert.fail(exception)
        finally:
            # Clean up app
            edit_app = dev_home.go_to_app_status_page(app)
            delete_popup = edit_app.click_delete_app()
            delete_popup.delete_app()

    @pytest.mark.credentials
    def test_hosted_app_submission(self, mozwebqa_devhub_logged_in):
        if '-dev.allizom' in mozwebqa_devhub_logged_in.base_url:
            env = 'dev'
        else:
            env = 'stage'

        app = MockApplication(env)

        dev_home = Home(mozwebqa_devhub_logged_in)

        dev_agreement = dev_home.click_submit_new_app()

        """Agree with the developer agreement and continue if it was not accepted
        in a previous app submit"""
        manifest_validation_form = dev_agreement.click_continue()

        # select device type
        for device in app['device_type']:
            if device[1]:
                manifest_validation_form.device_type(device[0])

        # submit the app manifest url and validate it
        manifest_validation_form.type_app_manifest_url(app['url'])
        manifest_validation_form.click_validate()
        Assert.true(manifest_validation_form.app_validation_status,
                    msg=manifest_validation_form.app_validation_message)

        app_details = manifest_validation_form.click_continue()
        Assert.true(app_details.is_the_current_submission_stage, '\n Expected step is: Details \n Actual step is: %s' % app_details.current_step)

        # add custom app details for every field
        app_details.click_change_name()
        app_details.type_url_end(app['url_end'])
        app_details.type_description(app['description'])
        app_details.type_privacy_policy(app['privacy_policy'])
        app_details.type_homepage(app['homepage'])
        app_details.type_support_url(app['support_website'])
        app_details.type_support_email(app['support_email'])

        for category in app['categories']:
            # check/uncheck the checkbox according to the app value
            app_details.select_categories(*category)

        app_details.screenshot_upload(app['screenshot_link'])
        try:
            next_steps = app_details.click_continue()
            Assert.equal('Almost There!', next_steps.almost_there_message)

            content_ratings = next_steps.click_continue()
            Assert.equal('Get My App Rated', content_ratings.get_app_rated_message)

            # insert Submission ID and Security code to get app rated
            content_ratings.fill_in_app_already_rated_info(app['submission_id'], app['security_code'])
            content_ratings.click_submit()
            Assert.equal('Congratulations, your app submission is now complete and will be reviewed shortly!',
                         content_ratings.saved_ratings_message)

        except Exception as exception:
            Assert.fail(exception)
        finally:
            # Clean up app
            edit_app = dev_home.go_to_app_status_page(app)
            delete_popup = edit_app.click_delete_app()
            delete_popup.delete_app()
