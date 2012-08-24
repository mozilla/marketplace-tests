#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from unittestzero import Assert


class BaseTest:
    """A base test class that can be extended by other tests to include utility methods."""

    def _login(self, mozwebqa, user=None):
        """login to consumer pages using the provided user
            if the user is not provided a new one will be created"""

        from pages.mobile.home import Home
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        if user == None:
            from mocks.mock_user import MockUser
            user = MockUser()
            home_page.create_new_user(user)

        home_page.login(user)

        return home_page, user
