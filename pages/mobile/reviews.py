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
    _success_notification_locator = (By.CSS_SELECTOR, 'section.notification-box.full > div.success')

    @property
    def is_success_message_visible(self):
        return self.is_element_visible(*self._success_notification_locator)
