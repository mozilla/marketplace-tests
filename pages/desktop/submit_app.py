#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pages.desktop.base import Base
from pages.page import Page


class SubmissionProcess(Base):
    #Base class that is available at every submission step
    _page_title = 'Submit an App | Developer Hub | Mozilla Marketplace'

    _continue_locator = (By.CSS_SELECTOR, '.continue.prominent')
    _current_step_locator = (By.CSS_SELECTOR, '#submission-progress > li.current')

    @property
    def current_step(self):
        return self.selenium.find_element(*self._current_step_locator).text

    @property
    def is_the_current_submission_stage(self):
        if self._page_title:
            WebDriverWait(self.selenium, 10).until(lambda s: self.selenium.title)

        from unittestzero import Assert
        Assert.equal(self.current_step, self._current_step,
            "Expected submission process stage is: %s. Actual submission process stage is: %s" % (self._current_step, self.current_step))
        return True

    def click_continue(self):
        current_step = self.current_step

        #Developer Agreement has a special worckflow
        if current_step == 'Developer Agreement' or not self.is_element_present(*self._continue_locator):
            # If the developer agrrement is not present then it was accepted
            # in a previos submit
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
    #The Developer Agreement step
    #This step is not available if it was accepted in a previous app submit
    _current_step = 'Developer Agreement'

    _dev_agreement_locator = (By.ID, 'dev-agreement')

    @property
    def is_dev_agreement_present(self):
            return self.is_element_present(*self._dev_agreement_locator)

class AppManifest(SubmissionProcess):
    #App manifest step
    #here the app maifest link is verified
    _current_step = 'App Manifest'

    _app_url_locator = (By.ID, 'upload-webapp-url')
    _app_validate_button_locator = (By.ID, 'validate_app')
    _continue_locator = (By.CSS_SELECTOR, 'button.upload-file-submit.prominent')
    _app_validation_status_locator = (By.CSS_SELECTOR, '#upload-status-results')

    def _wait_for_app_validation(self):
        WebDriverWait(self.selenium, 10).until(lambda s: self.is_element_present(*self._app_validation_status_locator), 'Validation process timed out')

    @property
    def app_validation_status(self):
        app_validation_status =self.selenium.find_element(*self._app_validation_status_locator).get_attribute('class')
        if app_validation_status == 'status-pass':
            return True
        return False

    @property
    def app_validation_message(self):
        _status_locator = (By.TAG_NAME, 'strong')
        _error_list_locator = (By.ID,'upload_errors')
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
    #App details step
    #here we complete all the info for the app
    _current_step = 'Details'

    _change_name_locator = (By.CSS_SELECTOR, 'div.before > span.edit')
    _name_locator = (By.ID, 'id_name')
    _url_end_locator = (By.ID, 'id_slug')
    _sumary_locator = (By.ID, 'id_summary_0')
    _categories_locator = (By.CSS_SELECTOR, 'ul.addon-categories > li')
    _description_locator = (By.ID, 'id_description_0')
    _pricacy_policy_locator = (By.ID, 'id_privacy_policy_0')
    _homepage_locator = (By.ID, 'id_homepage_0')
    _support_url_locator = (By.ID, 'id_support_url_0')
    _support_email_locator = (By.ID, 'id_support_email_0')
    _device_type_locator = (By.CSS_SELECTOR, '.brform.simple-field.c > ul > li')
    _screenshot_upload_locator = (By.CSS_SELECTOR, 'div.invisible-upload > input')
    _image_preview_locator = (By.CSS_SELECTOR, '#file-list div.preview-thumb.loading')

    @property
    def device_type(self):
        results = {}
        for category in self.selenium.find_elements(*self._device_type_locator):
            results[CheckBox(self.testsetup, category).name] = CheckBox(self.testsetup, category)
        return results

    @property
    def app_categories(self):
        results = {}
        for category in self.selenium.find_elements(*self._categories_locator):
            results[CheckBox(self.testsetup, category).name] = CheckBox(self.testsetup, category)
        return results

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
        text_fld = self.selenium.find_element(*self._pricacy_policy_locator)
        text_fld.clear()
        text_fld.send_keys(value)

    def type_descripion(self, value):
        text_fld = self.selenium.find_element(*self._description_locator)
        text_fld.clear()
        text_fld.send_keys(value)

    def type_summary(self, value):
        text_fld = self.selenium.find_element(*self._sumary_locator)
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
    #Payment options
    #here the payment type is selected
    _current_step = 'Payments'

    _payment_type_locator = (By.CSS_SELECTOR, 'div.brform.simple-field.c > ul > li')

    @property
    def payment_type(self):
        results = {}
        for category in self.selenium.find_elements(*self._payment_type_locator):
            results[CheckBox(self.testsetup, category).name] = CheckBox(self.testsetup, category)
        return results

class Finished(SubmissionProcess):
    #Final step that marks the end of the submission process
    _current_step = 'Finished!'

    _success_locator = (By.CSS_SELECTOR, '#submit-payment>h2')

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
        return self._root_element.find_element(*self._name_locator).text

    @property
    def state(self):
        return self._root_element.find_element(*self._check_box_locator).is_selected()

    def check(self):
        if self.state != True:
            self._root_element.find_element(*self._check_box_locator).click()

    def uncheck(self):
        if self.state == True:
            self._root_element.find_element(*self._check_box_locator).click()
