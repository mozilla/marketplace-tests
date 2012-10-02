#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from time import strptime, mktime

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from pages.desktop.developer_hub.base import Base
from pages.desktop.developer_hub.edit_app import EditListing
from pages.page import Page
from pages.page import PageRegion


class DeveloperSubmissions(Base):
    """
    Developer Submissions Page

    https://marketplace-dev.allizom.org/developers/submissions/
    """
    _page_title = "Manage My Submissions | Developers | Firefox Marketplace"

    _app_locator = (By.CSS_SELECTOR, 'div.items > div.item')
    _notification_locator = (By.CSS_SELECTOR, 'div.notification-box')

    def go_to_developer_hub(self):
        self.selenium.get('%s/developers/submissions' % self.base_url)

    @property
    def submitted_apps(self):
        return [App(self.testsetup, app) for app in self.selenium.find_elements(*self._app_locator)]

    @property
    def first_free_app(self):
        """Return the first free app in the listing."""
        for i in range(1, self.paginator.total_page_number + 1):
            for app in self.submitted_apps:
                if app.has_price and app.price == 'FREE':
                    return app
            if self.paginator.is_paginator_present:
                if not self.paginator.is_first_page_disabled:
                    self.paginator.click_next_page()
        else:
            raise Exception('App not found')

    def get_app(self, app_name):
        for i in range(1, self.paginator.total_page_number + 1):
            for app in self.submitted_apps:
                if app_name == app.name:
                    return app
            if self.paginator.is_paginator_present:
                if not self.paginator.is_first_page_disabled:
                    self.paginator.click_next_page()
        else:
            raise Exception('App not found')

    @property
    def is_notification_visibile(self):
        return self.is_element_visible(*self._notification_locator)

    @property
    def is_notification_succesful(self):
        return 'success' in self.find_element(*self._notification_locator).get_attribute('class')

    @property
    def notification_message(self):
        return  self.find_element(*self._notification_locator).text

    @property
    def sorter(self):
        return Sorter(self.testsetup)

    @property
    def paginator(self):
        from pages.desktop.regions.paginator import Paginator
        return Paginator(self.testsetup)


class App(PageRegion):

    _name_locator = (By.CSS_SELECTOR, 'h3')
    _incomplete_locator = (By.CSS_SELECTOR, 'p.incomplete')
    _created_date_locator = (By.CSS_SELECTOR, 'ul.item-details > li.date-created')
    _price_locator = (By.CSS_SELECTOR, 'ul.item-details > li > span.price')
    _edit_link_locator = (By.CSS_SELECTOR, 'a.action-link')
    _more_actions_locator = (By.CSS_SELECTOR, 'a.more-actions')
    _more_menu_locator = (By.CSS_SELECTOR, '.more-actions-popup')

    def _is_element_present_in_app(self, *locator):
        self.selenium.implicitly_wait(0)
        try:
            self.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
        finally:
            # set back to where you once belonged
            self.selenium.implicitly_wait(self.testsetup.default_implicit_wait)

    @property
    def is_incomplete(self):
        return self._is_element_present_in_app(*self._incomplete_locator)

    @property
    def name(self):
        return self.find_element(*self._name_locator).text

    @property
    def date(self):
        if not self.is_incomplete:
            date_text = self.find_element(*self._created_date_locator).text
            date = strptime(date_text.split(':')[1], ' %B %d, %Y')
            return mktime(date)

    @property
    def price(self):
        return self.find_element(*self._price_locator).text

    @property
    def has_price(self):
        return self._is_element_present_in_app(*self._price_locator)

    def click_edit(self):
        self.find_element(*self._edit_link_locator).click()
        return EditListing(self.testsetup)

    def click_more(self):
        if not self.is_more_menu_visible:
            self.find_element(*self._more_actions_locator).click()
            drop_down = self.selenium.find_elements(*self._more_menu_locator)
            return AppMoreOptions(self.testsetup, drop_down[-1])

    @property
    def is_more_menu_visible(self):
        return self.is_element_visible(*self._more_menu_locator)


class AppMoreOptions(PageRegion):

    _manage_status_locator = (By.CSS_SELECTOR, 'li > a')

    def click_option(self, lookup):
        for el in self.find_elements(*self._manage_status_locator):
            if el.text == lookup:
                el.click()
                return

    def click_manage_status(self):
        self.click_option("Manage Status")
        from pages.desktop.developer_hub.manage_status import ManageStatus
        return ManageStatus(self.testsetup)


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
