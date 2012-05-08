#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from pages.desktop.base import Base


class DeveloperHub(Base):
    """
    Developer Hub homepage

    https://marketplace-dev.allizom.org/developers/
    """
    _page_title = "Developer Hub | Mozilla Marketplace"

    def go_to_developer_hub(self):
        self.selenium.get('%s/developers/' % self.base_url)
