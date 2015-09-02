# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from pages.desktop.consumer_pages.base import Base


class Payment(Base):

    _page_title = 'Create PIN | Firefox Marketplace'

    _pin_container_locator = (By.CSS_SELECTOR, '.pinbox')
    _pin_continue_button_locator = (By.CSS_SELECTOR, '.cta')
    _pin_heading_locator = (By.CSS_SELECTOR, 'section.content h1')

    _app_name_locator = (By.CSS_SELECTOR, '.product .title')
    _buy_button_locator = (By.CSS_SELECTOR, '.cta.button.ltchk')

    def __init__(self, testsetup):
        Base.__init__(self, testsetup)

        if self.selenium.title != self._page_title:
            for handle in self.selenium.window_handles:
                self.selenium.switch_to_window(handle)
                WebDriverWait(self.selenium, self.timeout).until(lambda s: s.title)
        else:
            raise Exception('Page has not loaded')

    def click_buy_button(self):
        self.selenium.find_element(*self._buy_button_locator).click()
        # The window disappears after clicking the buy button,
        # so switch back to the original window
        WebDriverWait(self.selenium, self.timeout).until(lambda s: len(s.window_handles) == 1)
        self.selenium.switch_to_window(self.selenium.window_handles[0])

    @property
    def app_name(self):
        return self.selenium.find_element(*self._app_name_locator).text

    def create_pin(self, pin):
        self.wait_for_element_visible(*self._pin_container_locator)
        pin_input = self.selenium.find_element(*self._pin_container_locator)

        WebDriverWait(self.selenium, self.timeout).until(lambda s: 'Create' in self.pin_heading)
        # pin_input.send_keys() doesn't work, but the ActionChain does
        ActionChains(self.selenium).move_to_element(pin_input).send_keys(pin).perform()
        self.click_pin_continue()

        WebDriverWait(self.selenium, self.timeout).until(lambda m: 'Confirm' in self.pin_heading)
        ActionChains(self.selenium).move_to_element(pin_input).send_keys(pin).perform()
        self.click_pin_continue()

    @property
    def pin_heading(self):
        return self.selenium.find_element(*self._pin_heading_locator).text

    def click_pin_continue(self):
        button = self.selenium.find_element(*self._pin_continue_button_locator)
        WebDriverWait(self.selenium, self.timeout).until(lambda m: button.is_enabled())
        button.click()

    def wait_for_buy_app_section_displayed(self):
        self.wait_for_element_visible(*self._buy_button_locator)
