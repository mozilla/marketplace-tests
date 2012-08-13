#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

    _delete_app_locator = (By.ID, 'delete-addon')
    _delete_popup_locator = (By.ID, 'modal-delete')

    def click_delete_app(self):
        self.selenium.find_element(*self._delete_app_locator).click()

        WebDriverWait(self.selenium, 10).until(lambda s: self.is_element_visible(*self._delete_popup_locator))
        return DeleteAppPopUp(self.testsetup, self.find_element(*self._delete_popup_locator))


class DeleteAppPopUp(PageRegion):

    _delete_locator = (By.CSS_SELECTOR, 'button.delete-button')
    _cancel_locator = (By.CSS_SELECTOR, 'button.close.cancel')

    def delete_app(self):
        self.find_element(*self._delete_locator).click()
        from pages.desktop.developer_hub.developer_submissions import DeveloperSubmissions
        return DeveloperSubmissions(self.testsetup)

    def cancel_delete(self):
        self.find_element(*self._cancel_locator).click()
