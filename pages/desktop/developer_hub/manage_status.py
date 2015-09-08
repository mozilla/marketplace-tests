# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.page import PageRegion
from pages.desktop.developer_hub.base import Base


class ManageStatus(Base):
    """
    Edit Listing Master Page
    https://marketplace-dev.allizom.org/en-US/developers/app/{app_name}/status
    """

    _new_version_status_locator = (By.CSS_SELECTOR, '#version-list .status-pending > b')
    _previous_version_status_locator = (By.CSS_SELECTOR, '.status-disabled > b')
    _delete_app_locator = (By.ID, 'delete-addon')
    _delete_popup_locator = (By.ID, 'modal-delete')
    _app_not_found_message_locator = (By.CSS_SELECTOR, '#page section.primary h1')
    _upload_new_version_locator = (By.ID, 'upload-app')
    _loading_locator = (By.CSS_SELECTOR, 'div.item.island.loading')
    _upload_app = (By.ID, 'upload-app')
    _continue_button_locator = (By.ID, 'submit-upload-file-finish')
    _app_validation_status_locator = (By.ID, 'upload-status-results')
    _release_notes_locator = (By.ID, 'id_releasenotes_0')
    _save_changes_button_locator = (By.CSS_SELECTOR, 'button[type="submit"]')
    _notification_message_locator = (By.CSS_SELECTOR, '.notification-box.success')
    _new_packaged_version_locator = (By.CSS_SELECTOR, '#version-list tr:nth-child(1) h4 a')

    @property
    def app_not_found_message(self):
        return self.selenium.find_element(*self._app_not_found_message_locator).text

    def click_delete_app(self):
        self.selenium.find_element(*self._delete_app_locator).click()

        WebDriverWait(self.selenium, 10).until(lambda s: self.is_element_visible(*self._delete_popup_locator))
        return DeleteAppPopUp(self.testsetup, self.find_element(*self._delete_popup_locator))

    def click_upload_new_version(self):
        self.selenium.find_element(*self._upload_new_version_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(lambda s: not self.is_element_present(*self._loading_locator)
                                                         and self.selenium.execute_script('return jQuery.active == 0'))

    def upload_file(self, zip_file):
        self.selenium.find_element(*self._upload_app).send_keys(zip_file)

    def click_continue(self):
        self.selenium.find_element(*self._continue_button_locator).click()

    def wait_for_app_validation(self):
        WebDriverWait(self.selenium, self.timeout).until(lambda s:
                                                         self.is_element_visible(*self._app_validation_status_locator),
                                                         'Validation process timed out')

    def type_release_notes(self, value):
        self.type_in_element(self._release_notes_locator, value)

    def click_save_changes(self):
        self.selenium.find_element(*self._save_changes_button_locator).click()

    @property
    def notification_message(self):
        return self.selenium.find_element(*self._notification_message_locator).text

    @property
    def new_packaged_version(self):
        return self.selenium.find_element(*self._new_packaged_version_locator).text

    @property
    def new_version_status_message(self):
        return self.selenium.find_element(*self._new_version_status_locator).text

    @property
    def previous_version_status_message(self):
        return self.selenium.find_element(*self._previous_version_status_locator).text


class DeleteAppPopUp(PageRegion):

    _delete_locator = (By.CSS_SELECTOR, 'button.delete-button')
    _cancel_locator = (By.CSS_SELECTOR, 'button.close.cancel')

    def delete_app(self):
        self.find_element(*self._delete_locator).click()
        from pages.desktop.developer_hub.developer_submissions import DeveloperSubmissions
        return DeveloperSubmissions(self.testsetup)

    def cancel_delete(self):
        self.find_element(*self._cancel_locator).click()
