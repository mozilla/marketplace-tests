# coding: utf-8

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from mocks.mock_application import MockApplication
from pages.desktop.developer_hub.home import Home
from tests.base_test import BaseTest


class TestDeveloperHubSubmitApps(BaseTest):

    @pytest.mark.credentials
    def test_packaged_app_submission(self, mozwebqa, login_new):
        if '-dev.allizom' in mozwebqa.base_url:
            env = 'dev'
        else:
            env = 'stage'

        app = MockApplication(env, app_type='packaged')

        dev_home = Home(mozwebqa)

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
        assert manifest_validation_form.app_validation_status, manifest_validation_form.app_validation_message

        app_details = manifest_validation_form.click_continue()
        assert app_details.is_the_current_submission_stage, 'Expected step is: Details\nActual step is: %s' % app_details.current_step

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
            assert 'Almost There!' == next_steps.almost_there_message

            content_ratings = next_steps.click_continue()
            assert 'Get My App Rated' == content_ratings.get_app_rated_message

            # insert Submission ID and Security code to get app rated
            content_ratings.fill_in_app_already_rated_info(app['submission_id'], app['security_code'])
            content_ratings.click_submit()
            assert 'Congratulations, your app submission is now complete and will be reviewed shortly!' == content_ratings.saved_ratings_message
        finally:
            # Clean up app
            edit_app = dev_home.go_to_app_status_page(app)
            delete_popup = edit_app.click_delete_app()
            delete_popup.delete_app()

    @pytest.mark.xfail(reason='https://github.com/mozilla/marketplace-tests/issues/741')
    @pytest.mark.credentials
    def test_hosted_paid_app_submission(self, mozwebqa, login_new):
        if '-dev.allizom' in mozwebqa.base_url:
            env = 'dev'
        else:
            env = 'stage'

        app = MockApplication(env)

        dev_home = Home(mozwebqa)

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
        assert manifest_validation_form.app_validation_status, manifest_validation_form.app_validation_message
        try:
            app_details = manifest_validation_form.click_continue()
            assert app_details.is_the_current_submission_stage, 'Expected step is: Details\nActual step is: %s' % app_details.current_step

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

            next_steps = app_details.click_continue()
            assert 'Almost There!' == next_steps.almost_there_message

            content_ratings = next_steps.click_continue()
            assert 'Get My App Rated' == content_ratings.get_app_rated_message

            # insert Submission ID and Security code to get app rated
            content_ratings.fill_in_app_already_rated_info(app['submission_id'], app['security_code'])
            content_ratings.click_submit()
            assert 'Content ratings successfully saved.' == content_ratings.saved_ratings_message

            # setup payments
            payments = content_ratings.click_setup_payments()

            # add a payment account
            payments.add_payment_account()

            # select payment account
            payments.select_payment_account()

            # setup price tier
            app_price = '0.99 USD'
            payments.select_price(app_price)

            payments.click_payments_save_changes()
            assert payments.is_update_notification_visible
            assert app_price == payments.app_price
        finally:
            # Clean up app
            edit_app = dev_home.go_to_app_status_page(app)
            delete_popup = edit_app.click_delete_app()
            delete_popup.delete_app()

    @pytest.mark.credentials
    def test_hosted_app_submission(self, mozwebqa, login_new):
        if '-dev.allizom' in mozwebqa.base_url:
            env = 'dev'
        else:
            env = 'stage'

        app = MockApplication(env)

        dev_home = Home(mozwebqa)

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
        assert manifest_validation_form.app_validation_status, manifest_validation_form.app_validation_message
        try:
            app_details = manifest_validation_form.click_continue()
            assert app_details.is_the_current_submission_stage, 'Expected step is: Details\nActual step is: %s' % app_details.current_step

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

            next_steps = app_details.click_continue()
            assert 'Almost There!' == next_steps.almost_there_message

            content_ratings = next_steps.click_continue()
            assert 'Get My App Rated' == content_ratings.get_app_rated_message

            # insert Submission ID and Security code to get app rated
            content_ratings.fill_in_app_already_rated_info(app['submission_id'], app['security_code'])
            content_ratings.click_submit()
            assert 'Congratulations, your app submission is now complete and will be reviewed shortly!' == content_ratings.saved_ratings_message
        finally:
            # Clean up app
            edit_app = dev_home.go_to_app_status_page(app)
            delete_popup = edit_app.click_delete_app()
            delete_popup.delete_app()

    @pytest.mark.credentials
    def test_check_submission_of_an_app_with_XSS_in_its_app_name(self, mozwebqa, login_new):
        if '-dev.allizom' in mozwebqa.base_url:
            env = 'dev'
        else:
            env = 'stage'

        app = MockApplication(env, app_type='xss_app')

        dev_home = Home(mozwebqa)

        dev_agreement = dev_home.click_submit_new_app()

        """Agree with the developer agreement and continue if it was not accepted
        in a previous app submit"""
        manifest_validation_form = dev_agreement.click_continue()

        # select device type
        for device in app['device_type']:
            if device[1]:
                manifest_validation_form.device_type(device[0])

        manifest_validation_form.app_type(app['app_type'])

        # submit the app manifest url and validate it
        manifest_validation_form.type_app_manifest_url(app['url'])
        manifest_validation_form.click_validate()
        assert manifest_validation_form.app_validation_status, manifest_validation_form.app_validation_message
        try:
            app_details = manifest_validation_form.click_continue()
            assert app_details.is_the_current_submission_stage, 'Expected step is: Details\nActual step is: %s' % app_details.current_step

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

            next_steps = app_details.click_continue()
            assert 'Almost There!' == next_steps.almost_there_message

            content_ratings = next_steps.click_continue()
            assert 'Get My App Rated' == content_ratings.get_app_rated_message

            # insert Submission ID and Security code to get app rated
            content_ratings.fill_in_app_already_rated_info(app['submission_id'], app['security_code'])
            content_ratings.click_submit()
            assert 'Congratulations, your app submission is now complete and will be reviewed shortly!' == content_ratings.saved_ratings_message

            # check that xss is in app name
            edit_listing_page = dev_home.go_to_edit_listing_page(app)
            assert u"<script>alert('XSS')</script>" in edit_listing_page.page_title

            # check that xss name is in my submissions
            dev_submissions = edit_listing_page.left_nav_menu.click_my_submissions_menu()
            submitted_app_names = [first_app.name.lower() for first_app in dev_submissions.submitted_apps]
            assert u"<script>alert('xss')</script>" == submitted_app_names[0]
        finally:
            # Clean up app
            edit_app = dev_home.go_to_app_status_page(app)
            delete_popup = edit_app.click_delete_app()
            delete_popup.delete_app()

    @pytest.mark.credentials
    def test_new_version_submission_for_awaiting_review_app(self, mozwebqa, login_new):
        if '-dev.allizom' in mozwebqa.base_url:
            env = 'dev'
        else:
            env = 'stage'

        app = MockApplication(env, app_type='packaged')

        dev_home = Home(mozwebqa)

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

        # submit the packaged app and validate it
        manifest_validation_form.upload_file(app['app_path'])
        manifest_validation_form.wait_for_app_validation()

        assert manifest_validation_form.app_validation_status, manifest_validation_form.app_validation_message
        app_details = manifest_validation_form.click_continue()
        try:
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
            next_steps = app_details.click_continue()
            next_steps.click_continue()

            # Go to the Edit Page and add a new version
            manage_status = dev_home.go_to_app_status_page(app)
            new_version = MockApplication(app_type='new_version')

            manage_status.upload_file(new_version['app_path'])
            manage_status.wait_for_app_validation()
            manage_status.click_continue()
            assert 'New version successfully added.' == manage_status.notification_message
            manage_status.type_release_notes(new_version['description'])

            manage_status.click_save_changes()
            assert 'Version successfully edited.' == manage_status.notification_message
            assert '2.0' == manage_status.new_packaged_version
            assert 'Pending approval' == manage_status.new_version_status_message
            assert 'Obsolete' == manage_status.previous_version_status_message
        finally:
            # Clean up app
            edit_app = dev_home.go_to_app_status_page(app)
            delete_popup = edit_app.click_delete_app()
            delete_popup.delete_app()
