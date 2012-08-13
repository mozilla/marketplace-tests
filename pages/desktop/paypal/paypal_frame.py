#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from pages.page import Page

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class PayPalFrame(Page):

    _iframe_id = 'PPDGFrame'
    _iframe_locator = (By.ID, 'PPDGFrame')
    _paypal_login_button = (By.CSS_SELECTOR, 'div.logincnt p a.button.primary')

    def __init__(self, testsetup):
        Page.__init__(self, testsetup)
        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.is_element_visible(*self._iframe_locator))
        self.selenium.switch_to_frame(self._iframe_id)

    def login_to_paypal(self, user="sandbox"):

        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.wait_to_load)
        self.selenium.find_element(*self._paypal_login_button).click()

        from pages.desktop.paypal.paypal_popup import PayPalPopup
        pop_up = PayPalPopup(self.testsetup)
        pop_up.login_paypal(user)
        return PayPalPopup(self.testsetup)

    def wait_to_load(self):
        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.is_element_visible(*self._paypal_login_button))
