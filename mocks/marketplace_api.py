#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from unittestzero import Assert
from marketplace import Client
import json

DEFAULT_DOMAIN = 'marketplace-dev.allizom.org'


class MarketplaceAPI:

    def __init__(self, credentials=None, domain=None):
        consumer_key = credentials and credentials["key"] or None
        consumer_secret = credentials and credentials["secret"] or None
        domain= domain or DEFAULT_DOMAIN
        self._client = Client(
            domain=domain,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret)

    def submit_app(self, mock_app):

        #validate app manifest
        self._validate_manifest(mock_app)

        #create app
        self._create_app(mock_app)

        # update the app with the mock app data
        self.update_app_data(mock_app)

        # Add screenshot to app
        self.add_screenshot(mock_app)

        #change status to pending
        self.change_app_status_to_pending(mock_app)


    def _validate_manifest(self, mock_app):
        response = self._client.validate_manifest(mock_app['url'])
        manifest_validation_id =  json.loads(response.content)['id']

        # validate manifest
        validation_report = self._client.is_manifest_valid(manifest_validation_id)
        Assert.true(validation_report, "The manifest url is not valid.\n Validation report:\n %s" %validation_report)
        mock_app['manifest_validation_id'] = manifest_validation_id

    def _create_app(self, mock_app):
        # create app using the manifest
        response = self._client.create(mock_app.manifest_validation_id)

        Assert.equal(response.status_code, 201, "Invalid status code.\n Status code received is: %s" %response.status_code)
        mock_app['id'] = json.loads(response.content)['id']

    def update_app_data(self, mock_app):
        # update the default app data with the custom mock app information

        data = {
            'name': mock_app.name,
            'summary': mock_app.summary,
            'categories': [],
            'support_email': mock_app.support_email,
            'device_types': [],
            'payment_type': mock_app.payment_type,
            'premium_type': 'free',
            'privacy_policy': mock_app.privacy_policy,
            'description': mock_app.description,
            'homepage': mock_app.homepage,
            'support_url': mock_app.support_website
        }

        # device_types: a list of the device types at least one of: 'desktop', 'android-tablet', 'android-mobile', 'firefoxos'
        data['device_types'] = [device[0] for device in mock_app['device_type'] if device[1]]

        Assert.true(data['device_types'],  'insufficient data added device_types')

        # categories: a list of the categories, at least two of the category ids provided from the category api
        data['categories'] = [category['id'] for category in self._categories
                                if category['name'] in [mock_category[0] for mock_category in mock_app.categories]]

        Assert.greater_equal(len(data['categories']), 2,
            'Insufficient data added categories == %s\n Minimum 2 categories required' % data['categories'])

        response = self._client.update(mock_app.id, data)

        Assert.equal(response.status_code, 202, "Update app data failed.\n Status code %s" %response.status_code)

    def add_screenshot(self, mock_app):
        response = self._client.create_screenshot(app_id=mock_app.id, filename=mock_app["screenshot_link"], position=1)
        Assert.equal(response.status_code, 201,
            "Screenshot not valid.\n Status code %s\nResponse data %s" %(response.status_code, json.loads(response.content)))

    @property
    def _categories(self):
        return json.loads(self._client.get_categories().content)['objects']

    def delete_app(self, mock_app):
        # Not yet implemented: https://bugzilla.mozilla.org/show_bug.cgi?id=816572
        response = self._client.delete(mock_app.id)
        Assert.equal(response.status_code, 204, 'Delete app failed')

    def app_status(self, mock_app):
        response = self._client.status(mock_app.id)
        Assert.equal(response.status_code, 200, "App status failed\n Status code: %s" % response.status_code)

        return json.loads(response.content)

    @property
    def all_apps(self):
        response = self._client.list_webapps()

        Assert.equal(response.status_code, 200, "Get all apps failed\n Status code: %s" % response.status_code)
        return json.loads(response.content)['objects']

    def change_app_status_to_pending(self, mock_app):
        self.change_app_state(mock_app, state='pending')

    def change_app_state(self, mock_app, state):
        response = self._client.app_state(app_id=mock_app.id, status=state)
        Assert.equal(response.status_code, 202, "App state change failed\n Status code: %s" % response.status_code)
