#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from pages.desktop.consumer_pages.base import Base
from selenium.webdriver.common.by import By

from pages.page import Page


class Details(Base):
    """APP details page
    https://marketplace-dev.allizom.org/en-US/app/ app name
    app_name => the name of the app displayed
    """

    _purchase_locator = (By.CSS_SELECTOR, "section.product-details > div.actions > a.premium")
    _install_purchased_locator = (By.CSS_SELECTOR, "section.product-details > div.actions > a.premium.purchased.installing")
    _submit_review_link_locator = (By.ID, 'add-first-review')
    _statistics_link_locator = (By.CSS_SELECTOR, "p.view-stats a.arrow")
    
    _app_summary_locator = (By.CSS_SELECTOR, "p.summary")
    _app_expanded_description_locator = (By.CSS_SELECTOR, "div.more")
    _expand_description_locator = (By.CSS_SELECTOR, "a.collapse.wide")
    _collapse_description_locator = (By.CSS_SELECTOR, "a.collapse.wide.expanded.show")

    def __init__(self, testsetup, app_name = False):
        Base.__init__(self, testsetup)
        self.wait_for_ajax_on_page_finish()
        if app_name:
            self._page_title = "%s | Mozilla Marketplace" % app_name
            self.app_name = app_name

    @property
    def is_app_available_for_purchase(self):
        return self.is_element_visible(*self._purchase_locator)

    @property
    def is_app_installing(self):
        return self.is_element_visible(*self._install_purchased_locator)

    def click_purchase(self):
        self.selenium.find_element(*self._purchase_locator).click()
        return self.PreApproval(self.testsetup)

    def click_statistics(self):
        self.selenium.find_element(*self._statistics_link_locator).click()
        from pages.desktop.consumer_pages.statistics import Statistics
        return Statistics(self.testsetup)

    @property
    def is_submit_review_link_visible(self):
        return self.is_element_visible(*self._submit_review_link_locator)

    @property
    def submit_review_link(self):
        return self.selenium.find_element(*self._submit_review_link_locator).text

    def click_submit_review(self):
        self.selenium.find_element(*self._submit_review_link_locator).click()
        from pages.desktop.consumer_pages.add_review import AddReview
        return AddReview(self.testsetup, self.app_name)

    @property
    def app_summary_text(self):
        return self.selenium.find_element(*self._app_summary_locator).text

    @property
    def app_expanded_description_text(self):
        return self.selenium.find_element(*self._app_expanded_description_locator).text

    @property
    def is_app_description_expanded(self):
        return self.is_element_visible(*self._collapse_description_locator)
            
    def expand_app_description(self):
        self.selenium.find_element(*self._expand_description_locator).click()

    def collapse_app_description(self):
        self.selenium.find_element(*self._collapse_description_locator).click()

    class PreApproval(Page):
        _root_locator = (By.ID, 'pay')

        _one_time_payment_locator = (By.ID, 'payment-confirm')

        def __init__(self, testsetup):
            Page.__init__(self, testsetup)
            self._root_element = self.selenium.find_element(*self._root_locator)

        @property
        def is_visible(self):
            return self._root_element.is_displayed()

        def click_one_time_payment(self):
            self.selenium.find_element(*self._one_time_payment_locator).click()

            from pages.desktop.paypal.paypal_frame import PayPalFrame
            return PayPalFrame(self.testsetup)
