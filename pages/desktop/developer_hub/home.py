#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.desktop.developer_hub.base import Base


class Home(Base):

    _page_title = "My Apps | Mozilla Marketplace"

    _submit_new_app_locator = (By.CSS_SELECTOR, '.submit[href*=submit]')

    def go_to_developers_homepage(self):
        self.maximize_window()
        self.selenium.get("%s/developers/" % self.base_url)

    def go_to_app_status_page(self, app):
        self.selenium.get("%s/developers/app/%s/status" % (self.base_url, app['url_end']))
        from pages.desktop.developer_hub.manage_status import ManageStatus
        return ManageStatus(self.testsetup)

    def go_to_edit_listing_page(self, app):
        self.selenium.get("%s/developers/app/%s/edit" % (self.base_url, app['url_end']))
        from pages.desktop.developer_hub.edit_app import EditListing
        return EditListing(self.testsetup)

    def click_submit_new_app(self):
        self.selenium.find_element(*self._submit_new_app_locator).click()
        from pages.desktop.developer_hub.submit_app import DeveloperAgreement
        return DeveloperAgreement(self.testsetup)
