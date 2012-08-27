#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.page import Page
from pages.desktop.consumer_pages.base import Base


class AccountHistory(Base):

    _page_title = "Account History | Mozilla Marketplace"
    _purchased_apps_locator = (By.CSS_SELECTOR, '#purchases > ol.items > li.item')
    _notification_success_locator = (By.CSS_SELECTOR, 'section.notification-box > div.success')
    _notification_error_locator = (By.CSS_SELECTOR, 'section.notification-box > div.error')
    _account_history_title_locator = (By.CSS_SELECTOR, "#purchases > h1")
    _sort_by_locator = (By.CSS_SELECTOR, "#sorter > h3")
    _sort_purchase_date_locator = (By.CSS_SELECTOR, "#sorter > ul > li:nth-child(1)")
    _sort_price_locator = (By.CSS_SELECTOR, "#sorter > ul > li:nth-child(2)")
    _sort_name_locator = (By.CSS_SELECTOR, "#sorter > ul > li:nth-child(3)")
    _sort_selected_item_locator = (By.CSS_SELECTOR, "#sorter > ul > .selected")
    _purchased_applications_list_selector = (By.CSS_SELECTOR, "#purchases > .items > li")

    @property
    def purchased_apps(self):
        return [self.PurchasedApp(self.testsetup, web_element)
                for web_element in self.selenium.find_elements(*self._purchased_apps_locator)]

    @property
    def was_refund_successful(self):
        return self.is_element_visible(*self._notification_success_locator)

    @property
    def successful_notification_text(self):
        return self.selenium.find_element(*self._notification_success_locator).text

    @property
    def error_notification_text(self):
        try:
            return self.selenium.find_element(*self._notification_error_locator).text
        except :
            return ""

    @property
    def account_history_title(self):
        return self.selenium.find_element(*self._account_history_title_locator).text

    @property
    def sort_text(self):
        return self.selenium.find_element(*self._sort_by_locator).text

    @property
    def is_sort_by_item_visible(self):
        return self.is_element_visible(*self._sort_by_locator)

    @property
    def is_purchased_date_text_visible(self):
        return self.is_element_visible(*self._sort_purchase_date_locator)

    @property
    def purchased_date_text(self):
        return self.selenium.find_element(*self._sort_purchase_date_locator).text

    @property
    def selected_element(self):
        return self.selenium.find_element_by_css_selector("#sorter > ul > .selected").text

    @property
    def is_price_item_visible(self):
        return self.is_element_visible(*self._sort_price_locator)

    @property
    def price_item_text(self):
        return self.selenium.find_element(*self._sort_price_locator).text

    @property
    def is_name_item_visible(self):
        return self.is_element_visible(*self._sort_name_locator)

    @property
    def name_item_text(self):
        return self.selenium.find_element(*self._sort_name_locator).text

    @property
    def purchased_applications_count(self):
        return len(self.selenium.find_elements(*self._purchased_applications_list_selector))

    class PurchasedApp(Page):
        """provides the methods to access a purchased app
        self._root_element - webelement that points to a single result"""

        _name_locator = (By.CSS_SELECTOR, "div.info > h3 > a")
        _request_support_locator = (By.CSS_SELECTOR, "div.info > ul.vitals > li > a.request-support")
        _application_icon_locator = (By.CSS_SELECTOR, "#purchases > .items > li:nth-child(1) > .info > h3 > a > .icon")
        _application_description_locator = (By.CSS_SELECTOR, ".items > li > .info > p")
        _application_price_locator = (By.CSS_SELECTOR, ".items > li > .info > .vitals.c  > .vital.price")
        _application_categories_locator = (By.CSS_SELECTOR, ".items > li > .info > .vitals.c > span:nth-child(2)")
        _application_rating_locator = (By.CSS_SELECTOR, ".items > li > .info > .vitals.c > .rating")
        _application_weekly_downloads_locator = (By.CSS_SELECTOR, ".items > li > .info > .vitals.c > .vital.downloads")
        _application_premium_purchase_date_locator = (By.CSS_SELECTOR, "#purchases > .items > li > .info > .vitals.contributions > li > .purchase.supportable")
        _application_premium_support_link_locator = (By.CSS_SELECTOR, "#purchases > .items > li > .info > .vitals.contributions > li > .request-support")

        def __init__(self, testsetup, element):
            Page.__init__(self, testsetup)
            self._root_element = element

        @property
        def name(self):
            return self._root_element.find_element(*self._name_locator).text

        def click_name(self):
            self._root_element.find_element(*self._name_locator).click()
            from pages.desktop.consumer_pages.details import Details
            return Details(self.testsetup, self.name)

        def click_request_support(self):
            self._root_element.find_element(*self._request_support_locator).click()
            from pages.desktop.consumer_pages.app_support import AppSupport
            return AppSupport(self.testsetup)

        @property
        def is_application_icon_visible(self):
            return self.is_element_visible(*self._application_icon_locator)

        @property
        def is_application_name_visible(self):
            return self.is_element_visible(*self._name_locator)

        @property
        def is_application_description_visible(self):
            return self.is_element_visible(*self._application_description_locator)

        @property
        def is_application_price_visible(self):
            return self.is_element_visible(*self._application_price_locator)

        @property
        def application_price_text(self):
            return self.selenium.find_element(*self._application_price_locator).text

        @property
        def is_application_categories_section_visible(self):
            return self.is_element_visible(*self._application_categories_locator)

        @property
        def is_application_rating_section_visible(self):
            return self.is_element_visible(*self._application_rating_locator)

        @property
        def is_application_weekly_downloads_section_visible(self):
            return self.is_element_visible(*self._application_weekly_downloads_locator)

        @property
        def is_premium_application_purchased_date_visible(self):
            return self.is_element_visible(*self._application_premium_purchase_date_locator)

        @property
        def is_premium_application_support_link_visible(self):
            return self.is_element_visible(*self._application_premium_support_link_locator)
