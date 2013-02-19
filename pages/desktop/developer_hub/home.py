#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.desktop.developer_hub.base import Base


class Home(Base):

    _page_title = "My Apps | Mozilla Marketplace"
    _submit_app_locator = (By.CSS_SELECTOR, 'div.button-wrapper > .button.prominent')

    def go_to_developers_homepage(self):
        self.selenium.get("%s/developers/" % self.base_url)
        self.maximize_window()

    def click_submit_app(self):
        self.selenium.find_element(*self._submit_app_locator).click()
        from pages.desktop.developer_hub.submit_app import DeveloperAgreement
        return DeveloperAgreement(self.testsetup)
