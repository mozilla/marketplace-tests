#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from mocks.marketplace_api import MarketplaceAPI
from mocks.mock_application import MockApplication


@pytest.fixture(scope='function')
def mozwebqa_devhub_logged_in(request):
    from pages.desktop.developer_hub.home import Home
    mozwebqa = request.getfuncargvalue('mozwebqa')
    dev_home = Home(mozwebqa)
    dev_home.go_to_developers_homepage()
    dev_home.login(mozwebqa, user="default")

    return mozwebqa


@pytest.fixture(scope='function')
def free_app(request):
    """Return a free app created via the Marketplace API, and automatically delete the app after the test."""
    mozwebqa = request.getfuncargvalue('mozwebqa')
    request.app = MockApplication()
    api = MarketplaceAPI.get_client(mozwebqa.base_url,
                                    mozwebqa.credentials)
    api.submit_app(request.app)

    # This acts like a tearDown, running after each test function
    def fin():
        # If the app is being deleted by the test, set the id to 0
        if hasattr(request, 'app') and request.app['id'] > 0:
            api.delete_app(request.app)
    request.addfinalizer(fin)
    return request.app
