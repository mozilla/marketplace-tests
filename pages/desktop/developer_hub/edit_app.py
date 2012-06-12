#!/usr/bin/env python
# coding: utf-8

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.desktop.developer_hub.base import Base
from pages.desktop.developer_hub.submit_app import CheckBox
from pages.page import Page


class EditListing(Base):
    """Edit Listing master page"""
    _page_title = 'Edit Listing | {App name here} | Mozilla Marketplace'

    _edit_basic_info_locator = (By.CSS_SELECTOR, '#addon-edit-basic > h2 > a.button')
    _name_locator = (By.CSS_SELECTOR, 'div[data-name="name"]')
    _url_end_locator = (By.ID, 'slug_edit')
    _manifest_url_locator = (By.CSS_SELECTOR, '#manifest_url > td')
    _summary_locator = (By.CSS_SELECTOR, 'div[data-name="summary"]')
    _categories_locator = (By.CSS_SELECTOR, 'ul.addon-app-cats-inline > li')
    _device_types_locator = (By.ID, 'addon-device-types-edit')

    def click_edit_basic_info(self):
        self.selenium.find_element(*self._edit_basic_info_locator).click()
        return Details(self.testsetup)

    def matches_app_object(self, app):
        simple_values_match = (self.name == app['name'] and
                               app['url_end'] in self.url_end and
                               self.summary == app['summary'])
        categories_match = self.categories.encode('utf-8').split(' · ').sort() == app['categories'].sort()
        device_types_match = self.device_types.encode('utf-8').split(' · ').sort() == app['device_type'].sort()
        return simple_values_match and categories_match and device_types_match

    @property
    def name(self):
        return self.selenium.find_element(*self._name_locator).text

    @property
    def url_end(self):
        return self.selenium.find_element(*self._url_end_locator).text

    @property
    def manifest_url(self):
        return self.selenium.find_element(*self._manifest_url_locator).text

    @property
    def summary(self):
        return self.selenium.find_element(*self._summary_locator).text

    @property
    def categories(self):
        return self.selenium.find_element(*self._categories_locator).text

    @property
    def device_types(self):
        return self.selenium.find_element(*self._device_types_locator).text


class Details(EditListing):
    """Edit the details of the listing"""

    _name_locator = (By.ID, 'id_name_0')
    _url_end_locator = (By.ID, 'id_slug')
    _manifest_url_locator = (By.ID, 'manifest_url')
    # TODO: manifest should not be editable
    _summary_locator = (By.ID, 'id_summary_0')
    _categories_locator = (By.CSS_SELECTOR, 'ul.addon-categories > li')
    _device_type_locator = (By.CSS_SELECTOR, '#addon-device-types-edit > ul > li')
    _save_changes_locator = (By.CSS_SELECTOR, 'div.listing-footer > button')

    def select_device_type(self, name, state):
        for device in self.selenium.find_elements(*self._device_type_locator):
            device_type_checkbox = CheckBox(self.testsetup, device)
            if device_type_checkbox.name == name:
                if device_type_checkbox.state != state:
                    device_type_checkbox.change_state()

    def select_categories(self, name, state):
        for category in self.selenium.find_elements(*self._categories_locator):
            category_checkbox = CheckBox(self.testsetup, category)
            if category_checkbox.name == name:
                if category_checkbox.state != state:
                    category_checkbox.change_state()

    def type_summary(self, value):
        text_fld = self.selenium.find_element(*self._summary_locator)
        text_fld.clear()
        text_fld.send_keys(value)

    def type_url_end(self, value):
        text_fld = self.selenium.find_element(*self._url_end_locator)
        text_fld.clear()
        text_fld.send_keys(value)

    def type_name(self, value):
        text_fld = self.selenium.find_element(*self._name_locator)
        text_fld.clear()
        text_fld.send_keys(value)

    def click_save_changes(self):
        self.selenium.find_element(*self._save_changes_locator).click()
        return EditListing(self.testsetup)

