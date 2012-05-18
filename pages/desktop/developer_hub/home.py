#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.desktop.developer_hub.base import Base


class Home(Base):

    _page_title = "Developer Hub | Mozilla Marketplace"

    def go_to_homepage(self):
        self.selenium.get(self.base_url)
