# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest


@pytest.fixture
def login_existing(base_url, selenium, existing_user):
    from pages.desktop.developer_hub.home import Home
    home_page = Home(base_url, selenium)
    home_page.go_to_developers_homepage()
    home_page.login(existing_user['email'], existing_user['password'])


@pytest.fixture
def login_new(base_url, selenium, new_user):
    from pages.desktop.developer_hub.home import Home
    home_page = Home(base_url, selenium)
    home_page.go_to_developers_homepage()
    home_page.login(new_user['email'], new_user['password'])
