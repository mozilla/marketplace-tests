# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from urlparse import urlparse

from fxapom.fxapom import DEV_URL, FxATestAccount, PROD_URL
import pytest

from mocks.marketplace_api import MarketplaceAPI
from mocks.mock_application import MockApplication


@pytest.fixture
def fxa_test_account(mozwebqa):
    prod_hosts = ['marketplace.firefox.com', 'marketplace.allizom.org']
    api_url = PROD_URL if urlparse(mozwebqa.base_url).hostname in prod_hosts else DEV_URL
    return FxATestAccount(api_url)


@pytest.fixture
def new_user(fxa_test_account):
    return {'email': fxa_test_account.email,
            'password': fxa_test_account.password,
            'name': fxa_test_account.email.split('@')[0]}


@pytest.fixture
def stored_users(variables):
    return variables['users']


@pytest.fixture
def existing_user(stored_users):
    return stored_users['default']


@pytest.fixture
def api(existing_user, mozwebqa):
    host = urlparse(mozwebqa.base_url).hostname
    key = existing_user['api'][host]['key']
    secret = existing_user['api'][host]['secret']
    return MarketplaceAPI(key, secret, host)


@pytest.fixture
def free_app(request, api):
    """Return a free app created via the Marketplace API, and automatically delete the app after the test."""
    app = MockApplication()
    api.submit_app(app)

    def fin():
        if app['id'] > 0:
            api.delete_app(app)
    request.addfinalizer(fin)
    return app
