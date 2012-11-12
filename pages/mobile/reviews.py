#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By

from pages.mobile.base import Base


class Reviews(Base):
    """
    Page with all reviews of an app.
    """

    _data_body_class = 'reviews-listing'
    _notification_locator = (By.CSS_SELECTOR, 'section.notification-box div')

    @property
    def is_succesful_message(self):
        return 'success' in self.find_element(*self._notification_locator).get_attribute('class')

    @property
    def notification_message(self):
        return  self.find_element(*self._notification_locator).text

    def go_to_reviews_page(self, app):
        self.selenium.get('%s/app/%s/reviews/' % (self.base_url, app))
        self.app = app

    @property
    def _page_title(self):
        return 'Reviews for %s | Firefox Marketplace' % self.app
