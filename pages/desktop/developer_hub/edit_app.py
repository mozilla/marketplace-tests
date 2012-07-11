#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from unittestzero import Assert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.desktop.developer_hub.base import Base
from pages.desktop.developer_hub.submit_app import CheckBox


class EditListing(Base):
    """
    Edit Listing Master Page

    https://marketplace-dev.allizom.org/en-US/developers/app/{app_name}/edit
    """
    _edit_basic_info_locator = (By.CSS_SELECTOR, '#addon-edit-basic > h2 > a.button')
    _edit_support_information_locator = (By.CSS_SELECTOR, '#edit-addon-support .button')
    _edit_media_locator = (By.CSS_SELECTOR, '#edit-addon-media > h2 > a.button')
    _name_locator = (By.CSS_SELECTOR, 'div[data-name="name"]')
    _url_end_locator = (By.ID, 'slug_edit')
    _manifest_url_locator = (By.CSS_SELECTOR, '#manifest_url > td')
    _summary_locator = (By.CSS_SELECTOR, 'div[data-name="summary"]')
    _categories_locator = (By.CSS_SELECTOR, 'ul.addon-app-cats-inline > li')
    _device_types_locator = (By.ID, 'addon-device-types-edit')
    _save_changes_locator = (By.CSS_SELECTOR, 'div.listing-footer > button')
    _processing_panel_locator = (By.CSS_SELECTOR, 'div.island.loading')
    _email_locator = (By.CSS_SELECTOR, 'div[data-name="support_email"] span')
    _website_locator = (By.CSS_SELECTOR, 'div[data-name="support_url"] span')
    _icon_preview_img_locator = (By.CSS_SELECTOR, '#icon_preview_readonly > img')
    _screenshots_previews_locator = (By.CSS_SELECTOR, 'td.edit-previews-readonly > div > div.preview-successful')

    def __init__(self, testsetup):
        Base.__init__(self, testsetup)

        # Skip the explicit wait if EditListing is being inherited
        if not isinstance(self, (Media, SupportInformation, BasicInfo)):
            WebDriverWait(self.selenium, self.timeout).until(lambda s: self.is_element_visible(*self._screenshots_previews_locator))

    def click_edit_basic_info(self):
        self.selenium.find_element(*self._edit_basic_info_locator).click()
        return BasicInfo(self.testsetup)

    def click_support_information(self):
        self.selenium.find_element(*self._edit_support_information_locator).click()
        return SupportInformation(self.testsetup)

    def click_edit_media(self):
        self.selenium.find_element(*self._edit_media_locator).click()
        return Media(self.testsetup)

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

    @property
    def icon_preview_src(self):
        return self.selenium.find_element(*self._icon_preview_img_locator).get_attribute('src')

    @property
    def screenshots_previews(self):
        """Return a list of elements which represent screenshots that have been added to the app."""
        return self.selenium.find_elements(*self._screenshots_previews_locator)

    @property
    def no_forms_are_open(self):
        """Return true if no Save Changes buttons are visible."""
        if self.wait_for_element_not_present(*self._save_changes_locator):
            return True
        return False


class BasicInfo(EditListing):
    """
    Basic Information Edit Master Page

    The form that becomes active when editing basic information for an application listing.

    """
    _name_initial_locator = (By.ID, 'id_name_0')
    _name_after_failure_locator = (By.ID, 'id_name_1')
    _url_end_locator = (By.ID, 'id_slug')
    _manifest_url_locator = (By.CSS_SELECTOR, '#manifest-url > td > input')
    _summary_initial_locator = (By.ID, 'id_summary_0')
    _summary_after_failure_locator = (By.ID, 'id_summary_1')
    _summary_char_count_locator = (By.CSS_SELECTOR, 'div.char-count')
    _categories_locator = (By.CSS_SELECTOR, 'ul.addon-categories > li')
    _device_type_locator = (By.CSS_SELECTOR, '#addon-device-types-edit > ul > li')
    _name_error_locator = (By.CSS_SELECTOR, '#trans-name + ul.errorlist > li')
    _summary_error_locator = (By.CSS_SELECTOR, '#trans-summary + ul.errorlist > li')
    _url_end_error_locator = (By.CSS_SELECTOR, '#slug_edit ul.errorlist > li')
    _categories_error_locator = (By.CSS_SELECTOR, 'div.addon-app-cats > ul.errorlist > li')
    _device_types_error_locator = (By.CSS_SELECTOR, '#addon-device-types-edit > ul.errorlist > li')

    @property
    def is_this_form_open(self):
        """Return true if the Basic Info form is displayed."""
        return self.selenium.find_element(*self._url_end_locator).is_enabled()

    @property
    def is_summary_char_count_ok(self):
        """Return whether the character count for the summary field is reported as ok or not."""
        char_count = self.selenium.find_element(*self._summary_char_count_locator)
        return 'error' not in char_count.get_attribute('class')

    @property
    def name_error_message(self):
        """Return the error message displayed for the name."""
        return self.selenium.find_element(*self._name_error_locator).text

    @property
    def url_end_error_message(self):
        """Return the error message displayed for the url_end."""
        return self.selenium.find_element(*self._url_end_error_locator).text

    @property
    def summary_error_message(self):
        """Return the error message displayed for the summary."""
        return self.selenium.find_element(*self._summary_error_locator).text

    @property
    def categories_error_message(self):
        """Return the error message displayed for the categories."""
        return self.selenium.find_element(*self._categories_error_locator).text

    @property
    def device_types_error_message(self):
        """Return the error message displayed for the device types."""
        return self.selenium.find_element(*self._device_types_error_locator).text

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

    def clear_device_types(self):
        """Sets all device type checkboxes to unchecked"""
        for device in self.selenium.find_elements(*self._device_type_locator):
            device_type_checkbox = CheckBox(self.testsetup, device)
            if device_type_checkbox.state == True:
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

    def clear_categories(self):
        """Sets all category checkboxes to unchecked"""
        for device in self.selenium.find_elements(*self._categories_locator):
            device_type_checkbox = CheckBox(self.testsetup, device)
            if device_type_checkbox.state == True:
                device_type_checkbox.change_state()

    def type_name(self, text):
        if self.is_element_visible(*self._name_initial_locator):
            self.type_in_element(self._name_initial_locator, text)
        else:
            self.type_in_element(self._name_after_failure_locator, text)

    def type_url_end(self, text):
        self.type_in_element(self._url_end_locator, text)

    def type_summary(self, text):
        if self.is_element_visible(*self._summary_initial_locator):
            self.type_in_element(self._summary_initial_locator, text)
        else:
            self.type_in_element(self._summary_after_failure_locator, text)

    def type_manifest_url(self, text):
        self.type_in_element(self._manifest_url_locator, text)

    def click_save_changes(self, expected_result = 'success'):
        self.selenium.find_element(*self._save_changes_locator).click()

        if expected_result == 'success':
            return EditListing(self.testsetup)
        else:
            return BasicInfo(self.testsetup)


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
        return EditListing(self.testsetup)


class Media(EditListing):

    _icon_upload_locator = (By.ID, 'id_icon_upload')
    _icon_preview_64_image_locator = (By.CSS_SELECTOR, '#icon_preview_64 > img')
    _icon_preview_64_loading_locator = (By.CSS_SELECTOR, '#icon_preview_64.loading')
    _icon_preview_32_image_locator = (By.CSS_SELECTOR, '#icon_preview_32 > img')
    _icon_preview_32_loading_locator = (By.CSS_SELECTOR, '#icon_preview_32.loading')
    _icon_upload_error_message_locator = (By.CSS_SELECTOR, '#icon_preview ~ ul.errorlist > li')
    _screenshots_locator = (By.CSS_SELECTOR,
                            '#file-list > div.preview '
                            'div.preview-thumb[style^="background-image"]:not([class~="error-loading"])')
    _screenshot_upload_locator = (By.ID, 'screenshot_upload')
    _screenshot_loading_locator = (By.CSS_SELECTOR, 'div.preview-thumb.loading')
    _screenshot_upload_error_message_locator = (By.CSS_SELECTOR, 'div.edit-previews-text.error')
    _media_edit_cancel_link_locator = (By.CSS_SELECTOR, 'div.edit-media-button > a')

    @property
    def icon_preview_64_image_src(self):
        """Return the src attribute of the 64x64 icon."""
        return self.selenium.find_element(*self._icon_preview_64_image_locator).get_attribute('src')

    @property
    def icon_preview_32_image_src(self):
        """Return the src attribute of the 64x64 icon."""
        return self.selenium.find_element(*self._icon_preview_32_image_locator).get_attribute('src')

    @property
    def icon_upload_error_message(self):
        """Return the error message displayed for a failed icon upload."""
        return self.selenium.find_element(*self._icon_upload_error_message_locator).text

    @property
    def screenshots(self):
        """Return a list of elements that represent screenshots that have been uploaded for the app."""
        return self.selenium.find_elements(*self._screenshots_locator)

    @property
    def screenshot_upload_error_message(self):
        """Return the error message displayed for a failed screenshot upload."""
        return self.selenium.find_element(*self._screenshot_upload_error_message_locator).text

    def icon_upload(self, value):
        element = self.selenium.find_element(*self._icon_upload_locator)
        element.send_keys(value)
        self.wait_for_element_not_present(*self._icon_preview_64_loading_locator)
        self.wait_for_element_not_present(*self._icon_preview_32_loading_locator)

    def screenshot_upload(self, value):
        element = self.selenium.find_element(*self._screenshot_upload_locator)
        element.send_keys(value)
        self.wait_for_element_not_present(*self._screenshot_loading_locator)

    def click_save_changes(self, expected_result = 'success'):
        self.selenium.find_element(*self._save_changes_locator).click()

        if expected_result == 'success':
            return EditListing(self.testsetup)
        else:
            return Media(self.testsetup)

    def click_cancel(self):
        self.selenium.find_element(*self._media_edit_cancel_link_locator).click()
        return EditListing(self.testsetup)
