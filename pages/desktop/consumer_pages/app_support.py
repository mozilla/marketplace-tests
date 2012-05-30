#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.desktop.consumer_pages.base import Base


class AppSupport(Base):

    _request_refund_locator = (By.CSS_SELECTOR, '#support-start > li:nth-child(4) > a')

    def click_request_refund(self):
        self.selenium.find_element(*self._request_refund_locator).click()
        return RequestRefund(self.testsetup)


class RequestRefund(Base):
    _continue_locator = (By.CSS_SELECTOR, '#request-support > form > p.form-footer > button')

    def click_continue(self):
        self.selenium.find_element(*self._continue_locator).click()
        from pages.desktop.consumer_pages.account_history import AccountHistory
        return AccountHistory(self.testsetup)
