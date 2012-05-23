#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from time import strptime, mktime

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from pages.desktop.developer_hub.base import Base
from pages.page import Page


class DeveloperHub(Base):
    """
    Developer Hub homepage

    https://marketplace-dev.allizom.org/developers/
    """
    _page_title = "Developer Hub | Mozilla Marketplace"

    _app_locator = (By.CSS_SELECTOR, 'div.items > div.item')

    def go_to_developer_hub(self):
        self.selenium.get('%s/developers/' % self.base_url)

    @property
    def submited_apps(self):
        return [App(self.testsetup, app) for app in self.selenium.find_elements(*self._app_locator)]

    @property
    def sorter(self):
        return Sorter(self.testsetup)

    @property
    def paginator(self):
        from pages.desktop.regions.paginator import Paginator
        return Paginator(self.testsetup)


class App(Page):

    _name_locator = (By.CSS_SELECTOR, 'h3')
    _incomplete_locator = (By.CSS_SELECTOR, 'p.incomplete')
    _created_date_locator = (By.CSS_SELECTOR, 'ul.item-details > li.date-created')

    def __init__(self, testsetup, app):
        Page.__init__(self, testsetup)
        self.app = app

    @property
    def is_incomplete(self):
        self.selenium.implicitly_wait(0)
        try:
            self.app.find_element(*self._incomplete_locator)
            return True
        except NoSuchElementException:
            return False
        finally:
            # set back to where you once belonged
            self.selenium.implicitly_wait(self.testsetup.default_implicit_wait)

    @property
    def name(self):
        return self.app.find_element(*self._name_locator).text

    @property
    def date(self):
        if not self.is_incomplete:
            date_text = self.app.find_element(*self._created_date_locator).text
            date = strptime(date_text.split(':')[1], ' %B %d, %Y')
            return mktime(date)


class Sorter(Page):

    _sorter_base_locator = (By.ID, 'sorter')
    _options_locator = (By.CSS_SELECTOR, 'li > a.opt')
    _selected_locator = (By.CSS_SELECTOR, 'li.selected')

    def __init__(self, testsetup):
        Page.__init__(self, testsetup)
        self._sorter = self.selenium.find_element(*self._sorter_base_locator)

    @property
    def selected(self):
        return self._sorter.find_element(*self._selected_locator).text

    def sort_by(self, value):
        if not value == self.selected:
            for option in self._sorter.find_elements(*self._options_locator):
                if option.text.lower() == value.lower():
                    option.click()
