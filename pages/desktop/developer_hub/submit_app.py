#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

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
        if current_step == 'Developer Agreement' or not self.is_element_present(*self._continue_locator):
            # If the developer agreement is not present then it was accepted in a previous submit
            if self.is_dev_agreement_present:
                self.selenium.find_element(*self._continue_locator).click()
            return AppManifest(self.testsetup)
        else:
            # click continue and return the next logic step
            self.selenium.find_element(*self._continue_locator).click()
            if current_step == 'App Manifest':
                return Details(self.testsetup)
            elif current_step == 'Details':
                return Type(self.testsetup)
            elif current_step == 'Payments':
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


class AppManifest(SubmissionProcess):
    """App manifest step

    Here the app maifest link is verified"""
    _current_step = 'App Manifest'

    _precise_current_step_locator = (By.CSS_SELECTOR, '#submission-progress > li.manifest.current')
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

    _precise_current_step_locator = (By.CSS_SELECTOR, '#submission-progress > li.details.current')
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
    _premium_app = False

    _precise_current_step_locator = (By.CSS_SELECTOR, '#submission-progress > li.payments.current')

    def __init__(self, testsetup, premium_app=False):
        """
        class init method
        :Args:
         - premium_app - True/False
        """
        self._premium_app = premium_app
        SubmissionProcess.__init__(self, testsetup)

    def click_continue(self):
        url = self.get_url_current_page()
        self.selenium.find_element(*self._continue_locator).click()
        if self._premium_app:
            WebDriverWait(self.selenium, 10).until(lambda s: not url == self.get_url_current_page(), 'Page load timeout')
            url = self.get_url_current_page()
            if "upsell" in url:
                return UpSell(self.testsetup, self._premium_app)
            elif "paypal" in url:
                return PayPal(self.testsetup, self._premium_app)
            elif "bounce" in url:
                return Bounce(self.testsetup, self._premium_app)
            elif "confirm" in url:
                return ConfirmContactInformation(self.testsetup, self._premium_app)
            else:
                return Finished(self.testsetup)
        else:
            return Finished(self.testsetup)


class Type(Payments):

    _payment_type_locator = (By.CSS_SELECTOR, 'div.brform.simple-field.c > ul')

    def __init__(self, testsetup):
        Payments.__init__(self, testsetup)

    def select_payment_type(self, payment_type):
        if not payment_type == "Free":
            self._premium_app = True

        self.selenium.find_element(*self._payment_type_locator).\
            find_element(By.XPATH, "//li //label[normalize-space(text()) = '%s']" % payment_type).\
            click()


class UpSell(Payments):
    _price_selector_locator = (By.ID, 'id_price')
    _make_public_locator = (By.CSS_SELECTOR, ".brform.simple-field.c > ul > li > label[for^= 'id_make_public']")
    _do_upsell_locator = (By.CSS_SELECTOR, ".brform.simple-field.c > ul > li > label[for^= 'id_do_upsell']")
    _select_free_app_locator = (By.ID, 'id_free')
    _pitch_app_locator = (By.ID, 'id_text')

    def __init__(self, testsetup, premium_app=False):
        """
        class init method
        :Args:
         - premium_app - True/False
        """
        Payments.__init__(self, testsetup, premium_app)

    def select_price(self, value):
        price_selector = Select(self.selenium.find_element(*self._price_selector_locator))
        price_selector.select_by_visible_text(value)

    def make_public(self, value):
        """
        Method that accesses the "When should your app be made available for sale?" element
        :Args:
         - value - True/False to check the appropriate action
                  True = As soon as it is approved.
                  False = Not until I manually make it public.
        """

        make_public = self.selenium.find_elements(*self._make_public_locator)
        if value:
            make_public[0].click()
        else:
            make_public[1].click()

    def do_upsell(self, value):
        """
        Method that accesses the "Upsell this app" element
        :Args:
         - value - True/False to check the appropriate action
                  True = I don't have a free app to associate.
                  False = This is a premium upgrade.
        """
        up_sell = self.selenium.find_elements(*self._do_upsell_locator)
        if value:
            up_sell[0].click()
        else:
            up_sell[1].click()

    def select_free_app(self, value):
        """
        Method that accesses the "App to upgrade from" element
        :Args:
         - value - name of the free app you want to upgrade
        """
        free_app_selector = Select(self.selenium.find_element(*self._select_free_app_locator))
        free_app_selector.select_by_visible_text(value)

    def pitch_app(self, value):
        """
        Method that accesses the "Pitch your app" element
        :Args:
         - value - text that describes the app
        """
        self.type_in_element(self._pitch_app_locator, value)


class PayPal(Payments):
    _business_account_locator = (By.CSS_SELECTOR, 'div.brform.simple-field.c > ul')
    _paypal_email_locator = (By.ID, 'id_email')

    def __init__(self, testsetup, premium_app=False):
        """
        class init method
        :Args:
         - premium_app - True/False
        """
        Payments.__init__(self, testsetup, premium_app)

    def select_paypal_account(self, value):
        """
        Method that accesses the "Do you already have a PayPal Premier or Business account? " element
        :Args:
         - value - value to check: ["Yes", "No", "I'll link my PayPal account later."]
        """

        self.selenium.find_element(*self._business_account_locator).\
            find_element(By.XPATH, "//li //label[normalize-space(text()) = '%s']" % value).\
            click()

    def paypal_email(self, value):
        """
        Method that accesses the "PayPal email address" element
        :Args:
         - value - string containing a email address
        """
        self.type_in_element(self._paypal_email_locator, value)


class Bounce(Payments):
    _setup_permissions_locator = (By.CSS_SELECTOR, 'div.brform.island.swagger.c.devhub-form > a.button.prominent')

    def __init__(self, testsetup, premium_app=False):
        """
        class init method
        :Args:
         - premium_app - True/False
        """
        Payments.__init__(self, testsetup, premium_app)

    def click_setup_permissions(self):
        self.selenium.find_element(*self._setup_permissions_locator).click()
        from pages.desktop.paypal.paypal_permission_setup import PayPalPermissionsSandbox
        return PayPalPermissionsSandbox(self.testsetup)


class ConfirmContactInformation(Payments):

    _first_name_locator = (By.ID, 'id_first_name')
    _last_name_locator = (By.ID, 'id_last_name')
    _first_address_locator = (By.ID, 'id_address_one')
    _second_address_locator = (By.ID, 'id_address_tow')
    _city_locator = (By.ID, 'id_city')
    _state_locator = (By.ID, 'id_state')
    _post_code_locator = (By.ID, 'id_post_code')
    _country_locator = (By.ID, 'id_country')
    _phone_locator = (By.ID, 'id_phone')

    def __init__(self, testsetup, premium_app=False):
        """
        class init method
        :Args:
         - premium_app - True/False
        """
        Payments.__init__(self, testsetup, premium_app)

    def first_name(self, value):
        self.type_in_element(self._first_name_locator, value)

    def last_name(self, value):
        self.type_in_element(self._last_name_locator, value)

    def address(self, value):
        if len(value) > 255:
            self.type_in_element(self._first_name_locator, value[:255])
            self.type_in_element(self._second_address_locator, value[255:])
        else:
            self.type_in_element(self._first_name_locator, value)

    def city(self, value):
        self.type_in_element(self._city_locator, value)

    def state(self, value):
        self.type_in_element(self._state_locator, value)

    def post_code(self, value):
        self.type_in_element(self._post_code_locator, value)

    def country(self, value):
        self.type_in_element(self._country_locator, value)

    def phone(self, value):
        self.type_in_element(self._phone_locator, value)


class Finished(SubmissionProcess):
    """Final step that marks the end of the submission process"""
    _current_step = 'Finished!'

    _precise_current_step_locator = (By.CSS_SELECTOR, '#submission-progress > li.done.current')
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
