#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.page import Page
from pages.desktop.consumer_pages.base import Base


class AccountHistory(Base):

    _page_title = 'Account History | Firefox Marketplace'
    _purchased_apps_locator = (By.CSS_SELECTOR, '#purchases > ol.items > li.item')
    _notification_success_locator = (By.CSS_SELECTOR, 'section.notification-box > div.success')
    _notification_error_locator = (By.CSS_SELECTOR, 'section.notification-box > div.error')

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
        except:
            return ""

    class PurchasedApp(Page):
        """provides the methods to access a purchased app
        self._root_element - webelement that points to a single result"""

        _name_locator = (By.CSS_SELECTOR, 'div.info > h3 > a')
        _request_support_locator = (By.CSS_SELECTOR, 'div.info > ul.vitals > li > a.request-support')

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
