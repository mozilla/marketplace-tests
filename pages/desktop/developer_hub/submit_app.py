#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.desktop.developer_hub.base import Base
from pages.page import Page


class SubmissionProcess(Base):
    """Base class that is available at every submission step"""
    _page_title = 'Submit an App | Developer Hub | Mozilla Marketplace'

    _continue_locator = (By.CSS_SELECTOR, '.continue.prominent')
    _current_step_locator = (By.CSS_SELECTOR, '#submission-progress > li.current')

    @property
    def current_step(self):
        return self.selenium.find_element(*self._current_step_locator).text

    @property
    def is_the_current_submission_stage(self):
        """This mathod verifies if the current class is the same with the page we are in"""
        return self.current_step == self._current_step

    def click_continue(self):
        current_step = self.current_step

        #Developer Agreement has a special workflow
        if current_step == 'Developer Agreement' or not self.is_element_present(*self._continue_locator):
            #If the developer agreement is not present then it was accepted in a previous submit
            if self.is_dev_agreement_present:
                self.selenium.find_element(*self._continue_locator).click()
            return AppManifest(self.testsetup)
        else:
            #click continue and return the next logic step
            self.selenium.find_element(*self._continue_locator).click()
            if current_step == 'App Manifest':
                return Details(self.testsetup)
            elif current_step == 'Details':
                return Payments(self.testsetup)
            elif current_step == 'Payments':
                return Finished(self.testsetup)


class DeveloperAgreement(SubmissionProcess):
    """The Developer Agreement step

    This step is not available if it was accepted in a previous app submit"""
    _current_step = 'Developer Agreement'

    _dev_agreement_locator = (By.ID, 'dev-agreement')

    @property
    def is_dev_agreement_present(self):
            return self.is_element_present(*self._dev_agreement_locator)


class AppManifest(SubmissionProcess):
    """App manifest step

    Here the app maifest link is verified"""
    _current_step = 'App Manifest'

    _app_url_locator = (By.ID, 'upload-webapp-url')
    _app_validate_button_locator = (By.ID, 'validate_app')
    _continue_locator = (By.CSS_SELECTOR, 'button.upload-file-submit.prominent')
    _app_validation_status_locator = (By.CSS_SELECTOR, '#upload-status-results')

    def _wait_for_app_validation(self):
        WebDriverWait(self.selenium, 10).until(lambda s: self.is_element_present(*self._app_validation_status_locator), 'Validation process timed out')

    @property
    def app_validation_status(self):
        app_validation_status = self.selenium.find_element(*self._app_validation_status_locator).get_attribute('class')
        if app_validation_status == 'status-pass':
            return True
        return False

    @property
    def app_validation_message(self):
        _status_locator = (By.TAG_NAME, 'strong')
        _error_list_locator = (By.ID, 'upload_errors')
        app_validation_report = self.selenium.find_element(*self._app_validation_status_locator)
        result = {}
        result['status'] = app_validation_report.find_element(*_status_locator).text
        result['errors'] = app_validation_report.find_element(*_error_list_locator).text

        return result

    def type_app_manifest_url(self, value):
        text_fld = self.selenium.find_element(*self._app_url_locator)
        text_fld.clear()
        text_fld.send_keys(value)

    def click_validate(self):
        self.selenium.find_element(*self._app_validate_button_locator).click()
        self._wait_for_app_validation()


class Details(SubmissionProcess):
    """App details step
    here we complete all the info for the app"""
    _current_step = 'Details'

    _change_name_locator = (By.CSS_SELECTOR, 'div.before > span.edit')
    _name_locator = (By.ID, 'id_name')
    _url_end_locator = (By.ID, 'id_slug')
    _summary_locator = (By.ID, 'id_summary_0')
    _categories_locator = (By.CSS_SELECTOR, 'ul.addon-categories > li')
    _description_locator = (By.ID, 'id_description_0')
    _privacy_policy_locator = (By.ID, 'id_privacy_policy_0')
    _homepage_locator = (By.ID, 'id_homepage_0')
    _support_url_locator = (By.ID, 'id_support_url_0')
    _support_email_locator = (By.ID, 'id_support_email_0')
    _device_type_locator = (By.CSS_SELECTOR, '.brform.simple-field.c > ul > li')
    _screenshot_upload_locator = (By.CSS_SELECTOR, 'div.invisible-upload > input')
    _image_preview_locator = (By.CSS_SELECTOR, '#file-list div.preview-thumb.loading')

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

    def type_support_email(self, value):
        text_fld = self.selenium.find_element(*self._support_email_locator)
        text_fld.clear()
        text_fld.send_keys(value)

    def type_support_url(self, value):
        text_fld = self.selenium.find_element(*self._support_url_locator)
        text_fld.clear()
        text_fld.send_keys(value)

    def type_homepage(self, value):
        text_fld = self.selenium.find_element(*self._homepage_locator)
        text_fld.clear()
        text_fld.send_keys(value)

    def type_privacy_policy(self, value):
        text_fld = self.selenium.find_element(*self._privacy_policy_locator)
        text_fld.clear()
        text_fld.send_keys(value)

    def type_descripion(self, value):
        text_fld = self.selenium.find_element(*self._description_locator)
        text_fld.clear()
        text_fld.send_keys(value)

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

    def screenshot_upload(self, value):
        element = self.selenium.find_element(*self._screenshot_upload_locator)
        element.send_keys(value)
        WebDriverWait(self.selenium, self.timeout).until_not(lambda s: self.is_element_visible(*self._image_preview_locator), 'image is not loaded')

    def click_change_name(self):
        self.selenium.find_element(*self._change_name_locator).click()


class Payments(SubmissionProcess):
    """Payment options
    here the payment type is selected"""
    _current_step = 'Payments'

    _payment_type_locator = (By.CSS_SELECTOR, 'div.brform.simple-field.c > ul')

    def select_payment_type(self, payment_type):
        self.selenium.find_element(*self._payment_type_locator).\
            find_element(By.XPATH, "//li //label[normalize-space(text()) = '%s']" %payment_type).\
            click()


class Finished(SubmissionProcess):
    """Final step that marks the end of the submission process"""
    _current_step = 'Finished!'

    _success_locator = (By.CSS_SELECTOR, '#submit-payment > h2')

    @property
    def success_message(self):
        return self.selenium.find_element(*self._success_locator).text


class CheckBox(Page):

    _check_box_locator = (By.CSS_SELECTOR, 'label > input')
    _name_locator = (By.CSS_SELECTOR, 'label')

    def __init__(self, testsetup, root_element):
        Page.__init__(self, testsetup)
        self._root_element = root_element

    @property
    def name(self):
        '''returns the name (label) of the checkbox'''
        return self._root_element.find_element(*self._name_locator).text

    @property
    def state(self):
        '''returns the state of the checkbox:
            checked checkox returns True
            unchecked checbox returns False'''
        return self._root_element.find_element(*self._check_box_locator).is_selected()

    def change_state(self):
        '''changest the state of the checkbox:
            checked => unchecked
            unchecked => checked'''
        self._root_element.find_element(*self._check_box_locator).click()
