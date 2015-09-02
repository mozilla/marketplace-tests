#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.desktop.consumer_pages.home import Home


class BaseTest:
    """A base test class that can be extended by other tests to include utility methods."""

    def _get_resource_path(self, filename):
        """Return the path to the resources folder in the current repo."""
        import os
        path_to_resources_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources')
        return os.path.join(path_to_resources_folder, filename)

    def _open_payment_settings_page(self, current_page):
        """navigate to payment_settings_page from the current page"""

        # go to Payment Settings page
        settings_page = current_page.header.click_edit_account_settings()
        assert settings_page.is_the_current_page

        payment_settings_page = settings_page.click_payment_menu()
        assert 'Payment Settings' == payment_settings_page.header_title
        return payment_settings_page

    def _set_up_pre_approval(self, payment_settings_page):
        """Set up preapproval from payments settings page"""

        # request pre-approval
        paypal_sandbox = payment_settings_page.click_set_up_pre_approval()

        # login PayPal sandbox will throw a timeout error if login box doesn't appear
        paypal_sandbox.login_paypal_sandbox(user="sandbox")
        assert paypal_sandbox.is_user_logged_in

        # enact preapproval
        payment_settings_page = paypal_sandbox.click_approve_button()

        return payment_settings_page

    def _take_first_free_app_name(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        home_page.header.search(':free')
        app_name = home_page.first_app_name
        return app_name
