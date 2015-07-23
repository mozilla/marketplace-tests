#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from unittestzero import Assert
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class Page(object):
    '''
    Base class for all Pages
    '''

    _mobile_environment_locator = (By.CSS_SELECTOR, '.tab-link.mobile-cat-link')

    def __init__(self, testsetup):
        '''
        Constructor
        '''
        self.testsetup = testsetup
        self.base_url = testsetup.base_url
        self.selenium = testsetup.selenium
        self.timeout = testsetup.timeout
        self._selenium_root = hasattr(self, '_root_element') and self._root_element or self.selenium

    @property
    def is_the_current_page(self):
        if self._page_title:
            WebDriverWait(self.selenium, 10).until(lambda s: self.selenium.title)

        Assert.equal(self.selenium.title, self._page_title,
                     'Expected page title: %s. Actual page title: %s' % (
                         self._page_title, self.selenium.title))
        return True

    def is_element_present(self, *locator):
        self.selenium.implicitly_wait(0)
        try:
            self._selenium_root.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
        finally:
            # set back to where you once belonged
            self.selenium.implicitly_wait(self.testsetup.default_implicit_wait)

    def is_element_visible(self, *locator):
        try:
            return self._selenium_root.find_element(*locator).is_displayed()
        except (NoSuchElementException, ElementNotVisibleException):
            return False

    def is_element_not_visible(self, *locator):
        self.selenium.implicitly_wait(0)
        try:
            return not self._selenium_root.find_element(*locator).is_displayed()
        except (NoSuchElementException, ElementNotVisibleException):
            return True
        finally:
            # set back to where you once belonged
            self.selenium.implicitly_wait(self.testsetup.default_implicit_wait)

    def wait_for_element_visible(self, *locator):
        count = 0
        while not self.is_element_visible(*locator):
            time.sleep(1)
            count += 1
            if count == self.timeout:
                raise Exception(':'.join(locator) + " is not visible")

    def wait_for_element_not_visible(self, *locator):
        count = 0
        while self.is_element_visible(*locator):
            time.sleep(1)
            count += 1
            if count == self.timeout:
                raise Exception(':'.join(locator) + " is still visible")

    def wait_for_element_present(self, *locator):
        """Wait for an element to become present."""
        self.selenium.implicitly_wait(0)
        try:
            WebDriverWait(self.selenium, 10).until(lambda s: self._selenium_root.find_element(*locator))
        except TimeoutException:
            Assert.fail(TimeoutException)
        finally:
            # set back to where you once belonged
            self.selenium.implicitly_wait(self.testsetup.default_implicit_wait)

    def wait_for_element_not_present(self, *locator):
        """Wait for an element to become not present."""
        self.selenium.implicitly_wait(0)
        try:
            WebDriverWait(self.selenium, 10).until(lambda s: len(self._selenium_root.find_elements(*locator)) < 1)
            return True
        except TimeoutException:
            return False
        finally:
            # set back to where you once belonged
            self.selenium.implicitly_wait(self.testsetup.default_implicit_wait)

    def get_url_current_page(self):
        return self.selenium.current_url

    def refresh_page(self):
        return self.selenium.refresh()

    def type_in_element(self, locator, text):
        """
        Type a string into an element.

        This method clears the element first then types the string via send_keys.

        Arguments:
        locator -- a locator for the element
        text -- the string to type via send_keys

        """
        text_fld = self._selenium_root.find_element(*locator)
        text_fld.clear()
        text_fld.send_keys(text)

    def set_window_size(self):
        # Marketplace requires a minimum window width
        # to display elements that we are checking
        if self.selenium.get_window_size()['width'] < 1280:
            self.selenium.set_window_size(1280, 1024)

    def find_element(self, *locator):
        return self._selenium_root.find_element(*locator)

    def find_elements(self, *locator):
        return self._selenium_root.find_elements(*locator)

    @property
    def app_under_test(self):
        if self.is_element_visible(*self._mobile_environment_locator):
            return 'SoundCloud'
        else:
            return [
                'Wikipedia',
                'Calculator',
            ]

    def scroll_to_element(self, element):
        self.selenium.execute_script("window.scrollTo(0, %s)" % (element.location['y'] - element.size['height']))


class PageRegion(Page):

    def __init__(self, testsetup, element):
        self._root_element = element
        Page.__init__(self, testsetup)
