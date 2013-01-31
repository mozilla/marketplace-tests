#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

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
        """This method verifies if the current page is the one we expect to be on"""
        return self.is_element_visible(*self._precise_current_step_locator)

    def click_continue(self):
        current_step = self.current_step

        # Developer Agreement has a special work flow
        if current_step == 'Agreement' or not self.is_element_present(*self._continue_locator):
            # If the developer agreement is not present then it was accepted in a previous submit
            if self.is_dev_agreement_present:
                self.selenium.find_element(*self._continue_locator).click()
            return Validation(self.testsetup)
        else:
            # click continue and return the next logic step
            self.selenium.find_element(*self._continue_locator).click()
            if current_step == 'Submit':
                return Details(self.testsetup)
            elif current_step == 'Details':
                return Finished(self.testsetup)


class DeveloperAgreement(SubmissionProcess):
    """The Developer Agreement step

    This step is not available if it was accepted in a previous app submit"""
    _current_step = 'Developer Agreement'

    _precise_current_step_locator = (By.CSS_SELECTOR, '#submission-progress > li.terms.current')
    _dev_agreement_locator = (By.ID, 'dev-agreement')

    @property
    def is_dev_agreement_present(self):
        return self.is_element_present(*self._dev_agreement_locator)


class Submit(SubmissionProcess):
    """App manifest step"""

    _current_step = 'Submit'
    _precise_current_step_locator = (By.CSS_SELECTOR, '#submission-progress > li.manifest.current')


class Validation(Submit):
    """Here the app manifest link is verified"""
    _app_url_locator = (By.ID, 'upload-webapp-url')
    _app_validate_button_locator = (By.ID, 'validate_app')
    _continue_locator = (By.CSS_SELECTOR, 'button.upload-file-submit.prominent')
    _app_validation_status_locator = (By.ID, 'upload-status-results')
    _device_type_locator = (By.ID, 'free-%s')
    _hosted_app_locator = (By.CSS_SELECTOR, '#upload-file > hgroup > h2:nth-child(1)')
    _packaged_app_locator = (By.CSS_SELECTOR, '#upload-file > hgroup > h2:nth-child(2)')

    _upload_app = (By.ID, 'upload-app')

    def device_type(self, device_type):
        _device_locator = (self._device_type_locator[0], self._device_type_locator[1] % device_type)
        self.selenium.find_element(*_device_locator).click()

    def app_type(self, app_type):
        if app_type == 'hosted':
            self.selenium.find_element(*self._hosted_app_locator).click()
        else:
            self.selenium.find_element(*self._packaged_app_locator).click()

    def wait_for_app_validation(self):
        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.is_element_visible(*self._app_validation_status_locator), 'Validation process timed out')

    @property
    def app_validation_status(self):
        app_validation_status = self.selenium.find_element(*self._app_validation_status_locator).get_attribute('class')
        return app_validation_status == 'status-pass'

    @property
    def app_validation_message(self):
        _status_locator = (By.TAG_NAME, 'strong')
        _error_list_locator = (By.ID, 'upload_errors')
        app_validation_report = self.selenium.find_element(*self._app_validation_status_locator)

        result = {}
        result['status'] = app_validation_report.find_element(*_status_locator).text
        try:
            self.selenium.implicitly_wait(0)
            result['errors'] = app_validation_report.find_element(*_error_list_locator).text
            self.selenium.implicitly_wait(self.testsetup.default_implicit_wait)
        except NoSuchElementException:
                pass

        return result

    def type_app_manifest_url(self, value):
        self.type_in_element(self._app_url_locator, value)

    def upload_file(self, zip_file):
        self.selenium.find_element(*self._upload_app).send_keys(zip_file)

    def click_validate(self):
        self.selenium.find_element(*self._app_validate_button_locator).click()
        self.wait_for_app_validation()


class Details(SubmissionProcess):
    """App details step
    here we complete all the info for the app"""
    _current_step = 'Details'

    _precise_current_step_locator = (By.CSS_SELECTOR, '#submission-progress > li.details.current')
    _change_name_locator = (By.CSS_SELECTOR, 'div.before > span.edit')
    _name_locator = (By.ID, 'id_name')
    _url_end_locator = (By.ID, 'id_app_slug')
    _summary_locator = (By.ID, 'id_summary_0')
    _categories_locator = (By.CSS_SELECTOR, 'ul.addon-categories > li')
    _description_locator = (By.ID, 'id_description_0')
    _privacy_policy_locator = (By.ID, 'id_privacy_policy_0')
    _homepage_locator = (By.ID, 'id_homepage_0')
    _support_url_locator = (By.ID, 'id_support_url_0')
    _support_email_locator = (By.ID, 'id_support_email_0')
    _screenshot_upload_locator = (By.CSS_SELECTOR, 'div.invisible-upload > input')
    _image_preview_locator = (By.CSS_SELECTOR, '#file-list div.preview-thumb.loading')

    def select_categories(self, name, state):
        for category in self.selenium.find_elements(*self._categories_locator):
            category_checkbox = CheckBox(self.testsetup, category)
            if category_checkbox.name == name:
                if category_checkbox.state != state:
                    category_checkbox.change_state()

    def type_support_email(self, value):
        self.type_in_element(self._support_email_locator, value)

    def type_support_url(self, value):
        self.type_in_element(self._support_url_locator, value)

    def type_homepage(self, value):
        self.type_in_element(self._homepage_locator, value)

    def type_privacy_policy(self, value):
        self.type_in_element(self._privacy_policy_locator, value)

    def type_description(self, value):
        self.type_in_element(self._description_locator, value)

    def type_summary(self, value):
        self.type_in_element(self._summary_locator, value)

    def type_url_end(self, value):
        self.type_in_element(self._url_end_locator, value)

    def type_name(self, value):
        self.type_in_element(self._name_locator, value)

    def screenshot_upload(self, value):
        element = self.selenium.find_element(*self._screenshot_upload_locator)
        element.send_keys(value)
        WebDriverWait(self.selenium, self.timeout).until_not(lambda s: self.is_element_visible(*self._image_preview_locator), 'image is not loaded')

    def click_change_name(self):
        self.selenium.find_element(*self._change_name_locator).click()


class Finished(SubmissionProcess):
    """Final step that marks the end of the submission process"""
    _current_step = 'Finished!'

    _precise_current_step_locator = (By.CSS_SELECTOR, '#submission-progress > li.done.current')
    _success_locator = (By.CSS_SELECTOR, '#submit-done > h2')

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
