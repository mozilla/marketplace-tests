#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from unittestzero import Assert


class BaseTest:
    """A base test class that can be extended by other tests to include utility methods."""

    def _get_resource_path(self, filename):
        """Return the path to the resources folder in the current repo."""
        import os
        path_to_resources_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'resources')
        return os.path.join(path_to_resources_folder, filename)

    def _login_to_consumer_pages(self, mozwebqa, user=None):
        """login to consumer pages using the provided user
            if the user is not provided a new one will be created"""

        from pages.desktop.consumer_pages.home import Home
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        if user == None:
            from mocks.mock_user import MockUser
            user = MockUser()
            home_page.create_new_user(user)

        home_page.login(user)

        return home_page, user

    def _developer_page_login_to_paypal(self, mozwebqa):
        """login to PayPal developer pages"""

        from pages.desktop.paypal.paypal import PayPal
        developer_paypal_page = PayPal(mozwebqa)
        developer_paypal_page.go_to_page()
        developer_paypal_page.login_paypal(user="paypal")
        Assert.true(developer_paypal_page.is_user_logged_in)
        return developer_paypal_page

    def _open_payment_settings_page(self, current_page):
        """navigate to payment_settings_page from the current page"""

        # go to Payment Settings page
        settings_page = current_page.header.click_edit_account_settings()
        Assert.true(settings_page.is_the_current_page)

        payment_settings_page = settings_page.click_payment_menu()
        Assert.equal('Payment Settings', payment_settings_page.header_title)
        return payment_settings_page

    def _set_up_pre_approval(self, payment_settings_page):
        """Set up preapproval from payments settings page"""

        # request pre-approval
        paypal_sandbox = payment_settings_page.click_set_up_pre_approval()

        # login PayPal sandbox will throw a timeout error if login box doesn't appear
        paypal_sandbox.login_paypal_sandbox(user="sandbox")
        Assert.true(paypal_sandbox.is_user_logged_in)

        # enact preapproval
        payment_settings_page = paypal_sandbox.click_approve_button()

        return payment_settings_page

    def _delete_app(self, mozwebqa, app_name):
        from pages.desktop.developer_hub.home import Home
        dev_home = Home(mozwebqa)
        dev_home.go_to_developers_homepage()

        submitted_apps = dev_home.header.click_my_submissions()

        app = submitted_apps.get_app(app_name)

        manage_status = app.click_manage_status_and_versions()
        delete_popup = manage_status.click_delete_app()

        return delete_popup.delete_app()
