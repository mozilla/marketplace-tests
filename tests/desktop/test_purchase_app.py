#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest
from unittestzero import Assert

from pages.desktop.consumer_pages.home import Home
from pages.desktop.regions.filter import FilterTags
from mocks.mock_user import MockUser


class TestPurchaseApp:

    _app_name = "test webap"
    _web_app_search_term = "krupa"

    def test_that_purchases_an_app_without_pre_auth_and_requests_a_refund(self, mozwebqa):
        """Litmus 58166"""
        user = MockUser()
        home_page = Home(mozwebqa)

        home_page.go_to_homepage()
        home_page.create_new_user(user)
        home_page.login(user)

        Assert.true(home_page.is_the_current_page)

        search_page = home_page.header.search(self._app_name)
        Assert.true(search_page.is_the_current_page)

        Assert.not_equal("FREE", search_page.results[0].price)
        details_page = search_page.results[0].click_name()
        Assert.true(details_page.is_app_available_for_purchase)

        pre_aproval_region = details_page.click_purchase()

        paypal_frame = pre_aproval_region.click_one_time_payment()

        paypal_popup = paypal_frame.login_to_paypal()
        Assert.true(paypal_popup.is_user_logged_into_paypal)

        try:
            # From this point on we have payed for the app so we have to request a refund
            paypal_popup.click_pay()
            paypal_popup.close_paypal_popup()
            Assert.true(details_page.was_purchase_successful, details_page.purchase_error_message)
            Assert.true(details_page.is_app_installing)
        except Exception as exception:
            Assert.fail(exception)
        finally:
            if details_page.was_purchase_successful:
                self.request_refund_procedure(mozwebqa, self._app_name, user_account="buy_no_preapproval")

    def test_that_purchases_an_app_with_pre_auth_and_requests_a_refund(self, mozwebqa):
        """Litmus 58166"""

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        home_page.login("buy_preapproval")

        Assert.true(home_page.is_the_current_page)

        search_page = home_page.header.search(self._web_app_search_term)
        Assert.true(search_page.is_the_current_page)
        search_page.sort_by("Price")
        search_page.filter_by("Premium Only").click()

        Assert.not_equal("FREE", search_page.unpurchased_apps[0].price)
        app_name = search_page.unpurchased_apps[0].name
        details_page = search_page.unpurchased_apps[0].click_name()
        Assert.true(details_page.is_app_available_for_purchase)

        Assert.equal("PayPal pre-approval", details_page.preapproval_checkmark_text)
        try:
            details_page = details_page.click_purchase()

            Assert.true(details_page.is_app_purchasing)
            Assert.true(details_page.was_purchase_successful, details_page.purchase_error_message)
            Assert.true(details_page.is_app_installing)
        except Exception as exception:
            Assert.fail(exception)

        finally:
            if details_page.was_purchase_successful:
                self.request_refund_procedure(mozwebqa, app_name, user_account="buy_no_preapproval")


    def request_refund_procedure(self, mozwebqa, app_name, user_account="default"):
        """necessary steps to request a refund"""
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.true(home_page.is_the_current_page)
        Assert.true(home_page.footer.is_user_logged_in)

        account_history_page = home_page.footer.click_account_history()
        purchased_apps = account_history_page.purchased_apps

        for listed_app in purchased_apps:
            if listed_app.name == app_name:
                app_support_page = listed_app.click_request_support()
                break

        request_refund_page = app_support_page.click_request_refund()
        account_history_page = request_refund_page.click_continue()

        if not account_history_page.was_refund_successful and \
           account_history_page.error_notification_text == "There was an error with your instant refund.":
            pytest.xfail(reason="Bugzilla 769364 - IPN Updates refund table")

        Assert.true(account_history_page.was_refund_successful, account_history_page.error_notification_text)
        Assert.equal(account_history_page.successful_notification_text, "Refund is being processed.")
