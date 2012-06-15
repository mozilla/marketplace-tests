#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pages.desktop.developer_hub.base import Base
from pages.desktop.developer_hub.submit_app import CheckBox


class EditListing(Base):
    """
    Edit Listing Master Page

    https://marketplace-dev.allizom.org/en-US/developers/app/{app_name}/edit

    """
    _page_title = 'Edit Listing | {App name here} | Mozilla Marketplace'

    _edit_basic_info_locator = (By.CSS_SELECTOR, '#addon-edit-basic > h2 > a.button')
    _edit_support_information_locator = (By.CSS_SELECTOR, '#edit-addon-support .button')
    _name_locator = (By.CSS_SELECTOR, 'div[data-name="name"]')
    _url_end_locator = (By.ID, 'slug_edit')
    _manifest_url_locator = (By.CSS_SELECTOR, '#manifest_url > td')
    _summary_locator = (By.CSS_SELECTOR, 'div[data-name="summary"]')
    _categories_locator = (By.CSS_SELECTOR, 'ul.addon-app-cats-inline > li')
    _device_types_locator = (By.ID, 'addon-device-types-edit')

    _email_locator = (By.CSS_SELECTOR, 'div[data-name="support_email"] span')
    _website_locator = (By.CSS_SELECTOR, 'div[data-name="support_url"] span')

    def click_edit_basic_info(self):
        self.selenium.find_element(*self._edit_basic_info_locator).click()
        return BasicInfo(self.testsetup)

    def click_support_information(self):
        self.selenium.find_element(*self._edit_support_information_locator).click()
        return SupportInformation(self.testsetup)

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
        """Return a list of categories, utf-8 encoded."""
        return self.selenium.find_element(*self._categories_locator).text.encode('utf-8').split(' · ')

    @property
    def device_types(self):
        """Return a list of device types, utf-8 encoded."""
        return self.selenium.find_element(*self._device_types_locator).text.encode('utf-8').split(' · ')

    @property
    def email(self):
        return self.selenium.find_element(*self._email_locator).text

    @property
    def website(self):
        return self.selenium.find_element(*self._website_locator).text


class BasicInfo(EditListing):
    """
    Basic Information Edit Master Page

    The form that becomes active when editing basic information for an application listing.

    """
    _name_locator = (By.ID, 'id_name_0')
    _url_end_locator = (By.ID, 'id_slug')
    _manifest_url_locator = (By.CSS_SELECTOR, '#manifest-url > td > input')
    # TODO: manifest should not be editable
    _summary_locator = (By.ID, 'id_summary_0')
    _categories_locator = (By.CSS_SELECTOR, 'ul.addon-categories > li')
    _device_type_locator = (By.CSS_SELECTOR, '#addon-device-types-edit > ul > li')
    _save_changes_locator = (By.CSS_SELECTOR, 'div.listing-footer > button')

    def select_device_type(self, name, state):
        """Set the value of a single device type checkbox.

        Arguments:
        name -- the name of the checkbox to set
        state -- the state to leave the checkbox in

        """
        for device in self.selenium.find_elements(*self._device_type_locator):
            device_type_checkbox = CheckBox(self.testsetup, device)
            if device_type_checkbox.name == name:
                if device_type_checkbox.state != state:
                    device_type_checkbox.change_state()

    def select_categories(self, name, state):
        """Set the value of a single category checkbox.

        Arguments:
        name -- the name of the checkbox to set
        state -- the state to leave the checkbox in

        """
        for category in self.selenium.find_elements(*self._categories_locator):
            category_checkbox = CheckBox(self.testsetup, category)
            if category_checkbox.name == name:
                if category_checkbox.state != state:
                    category_checkbox.change_state()

    def type_summary(self, text):
        self.type_in_element(self._summary_locator, text)

    def type_url_end(self, text):
        self.type_in_element(self._url_end_locator, text)

    def type_name(self, text):
        self.type_in_element(self._name_locator, text)

    def type_manifest_url(self, text):
        self.type_in_element(self._manifest_url_locator, text)

    def click_save_changes(self):
        self.selenium.find_element(*self._save_changes_locator).click()
        WebDriverWait(self.selenium, 10).until(lambda s: self.is_element_present(*self._edit_basic_info_locator), 'Save changes process timed out')
        return EditListing(self.testsetup)


class SupportInformation(EditListing):

    _email_locator = (By.ID, 'id_support_email_0')
    _website_locator = (By.ID, 'id_support_url_0')
    _save_changes_locator = (By.CSS_SELECTOR, 'div.listing-footer > button')

    def type_support_email(self, text):
        self.type_in_element(self._email_locator, text)

    def type_support_url(self, text):
        self.type_in_element(self._website_locator, text)

    def click_save_changes(self):
        self.selenium.find_element(*self._save_changes_locator).click()
        WebDriverWait(self.selenium, 10).until(lambda s: self.is_element_present(*self._edit_basic_info_locator), 'Save changes process timed out')
        return EditListing(self.testsetup)
