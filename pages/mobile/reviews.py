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

    def go_to_reviews_page(self, app):
        self.selenium.get('%s/app/%s/reviews/' % (self.base_url, app))
        self.app = app

    @property
    def _page_title(self):
        return 'Reviews for %s | Firefox Marketplace' % self.app
