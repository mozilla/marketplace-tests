# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.desktop.developer_hub.base import Base
from pages.page import Page, PageRegion


class ContentTools(Base):

    _submit_new_add_on_button_locator = (By.CSS_SELECTOR, '.landing--submit a')
    _agree_button_locator = (By.CSS_SELECTOR, '.sign button')
    _submit_add_on_form_button_locator = (By.CSS_SELECTOR, '.addon-upload button[type="submit"]')
    _select_add_on_file_button_locator = (By.CLASS_NAME, 'form-inline--file-input')
    _add_on_file_input_locator = (By.ID, 'submission-addon--zip')
    _notification_message_locator = (By.CSS_SELECTOR, '.notification')
    _add_on_locator = (By.CSS_SELECTOR, 'li.addon-for-listing')

    @property
    def header(self):
        return self.HeaderRegion(self.base_url, self.selenium)

    @property
    def notification_message(self):
        return self.selenium.find_element(*self._notification_message_locator).text

    @property
    def add_ons(self):
        return [self.AddOn(self.base_url, self.selenium, web_element)
                for web_element in self.selenium.find_elements(*self._add_on_locator)]

    def add_on(self, name):
        return next(a for a in self.add_ons if a.name == name)

    def go_to_page(self):
        self.selenium.get(self.base_url + '/content')
        return self

    def click_submit_new_add_on(self):
        self.selenium.find_element(*self._submit_new_add_on_button_locator).click()
        el = self.selenium.find_element(*self._agree_button_locator)
        WebDriverWait(self.selenium, self.timeout).until(EC.visibility_of(el))

    def click_agree(self):
        self.selenium.find_element(*self._agree_button_locator).click()
        el = self.selenium.find_element(*self._select_add_on_file_button_locator)
        WebDriverWait(self.selenium, self.timeout).until(EC.visibility_of(el))

    def select_add_on_file(self, zip_file):
        file_input = self.selenium.find_element(*self._add_on_file_input_locator)
        # WARNING: This is a huge hack but is required in order to be able to send_keys
        # to the file input, which has an explicit top of -9999px
        self.selenium.execute_script('arguments[0].style.top = 0;', file_input)
        file_input.send_keys(zip_file)
        el = self.selenium.find_element(*self._select_add_on_file_button_locator)
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: el.get_attribute('data-file-input--has-data'))

    def click_submit_add_on_form_button(self):
        self.selenium.find_element(*self._submit_add_on_form_button_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(
            EC.visibility_of_element_located(self._notification_message_locator))

    class HeaderRegion(Page):

        _account_menu_locator = (By.CLASS_NAME, 'header-user-dropdown-toggle')
        _login_locator = (By.CSS_SELECTOR, '.header-user li:nth-of-type(2) button.login')

        @property
        def is_user_logged_in(self):
            return self.is_element_visible(*self._account_menu_locator)

        def click_login(self):
            self.selenium.find_element(*self._login_locator).click()
            from fxapom.pages.sign_in import SignIn
            return SignIn(self.selenium)

    class AddOn(PageRegion):

        _link_locator = (By.CSS_SELECTOR, '.addon-for-listing-metadata a')
        _status_locator = (By.CSS_SELECTOR, 'di[class^="addon--status"] dd')
        _delete_add_on_button_locator = (By.CSS_SELECTOR, '.addon-dashboard-detail--actions .button--delete')
        # Note: after clicking the above button once the text changes to "Are you sure?"
        _delete_confirmation_locator = (By.CSS_SELECTOR, 'main .page-section--main')

        @property
        def name(self):
            return self.find_element(*self._link_locator).text

        @property
        def status(self):
            return self.find_element(*self._status_locator).text

        def delete(self):
            self.find_element(*self._link_locator).click()
            WebDriverWait(self.selenium, self.timeout).until(
                EC.visibility_of_element_located(self._delete_add_on_button_locator))
            self.selenium.find_element(*self._delete_add_on_button_locator).click()
            WebDriverWait(self.selenium, self.timeout).until(
                EC.text_to_be_present_in_element(self._delete_add_on_button_locator, 'Are you sure'))
            self.selenium.find_element(*self._delete_add_on_button_locator).click()
            WebDriverWait(self.selenium, self.timeout).until(
                EC.text_to_be_present_in_element(self._delete_confirmation_locator, 'This add-on has been deleted'))
