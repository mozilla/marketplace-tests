#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from unittestzero import Assert

from pages.desktop.consumer_pages.home import Home


class TestPurchaseApp:

    _app_name = 'Campfire'

    def test_that_purchasess_an_app_without_pre_auth_and_requests_a_refund(self, mozwebqa):
        """Litmus 58166"""
        home_page = Home(mozwebqa)

        home_page.go_to_homepage()
        home_page.login()

        Assert.true(home_page.is_the_current_page)

        search_page = home_page.header.search(self._app_name)
        Assert.true(search_page.is_the_current_page)

        details_page = search_page.results[0].clcik_name()
        Assert.true(details_page.is_app_available_for_purchase)

        pre_aproval_region = details_page.click_purchase()

        paypal_frame = pre_aproval_region.click_one_time_payment()

        paypall_popup = paypal_frame.login_to_paypal()
        Assert.true(paypall_popup.is_user_logged_into_paypal)

        try:
            """From this point on we have payed for the app so we have to request a refund"""
            paypall_popup.click_pay()
            paypall_popup.close_paypal_popup()

            Assert.true(details_page.is_app_installing())
        except Exception as exception:
            Assert.fail(exception)
        finally:
            self.request_refund_procedure(mozwebqa, self._app_name)

    def request_refund_procedure(self, mozwebqa, app_name):
        """necessary steps to request a refund"""
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        if not home_page.footer.is_user_logged_in:
            home_page.login()
        Assert.true(home_page.is_the_current_page)
        Assert.true(home_page.footer.is_user_logged_in)

        account_history_page = home_page.footer.click_account_history()
        purchesed_apps = account_history_page.purchesed_apps

        stop = True
        idx = 0
        while stop:
            if purchesed_apps[idx].name == app_name:
                app_support_page = purchesed_apps[idx].click_request_support()

                request_refund_page = app_support_page.click_request_refund()
                account_history_page = request_refund_page.click_continue()
                stop = False
            else:
                idx = idx + 1

        Assert.equal(account_history_page.succsessful_notification_text, "Refund is being processed.")
