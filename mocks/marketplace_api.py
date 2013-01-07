#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from unittestzero import Assert
from marketplace import Client
import json

MARKETPLACE_DOMAIN = 'marketplace-dev.allizom.org'


class MarketplaceAPI:

    def __init__(self, credentials=None, domain=None):
        consumer_key = credentials and credentials["key"] or None
        consumer_secret = credentials and credentials["secret"] or None
        domain= domain or MARKETPLACE_DOMAIN
        self._client = Client(
            domain=domain,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret)

    def _validate_manifest(self, mock_app_url):
        response = self._client.validate_manifest(mock_app_url)
        self.manifest_id = json.loads(response.content)['id']
        return self.manifest_id

    def submit_app(self, mock_app):
        # Get the manifest validation result id
        manifest_validation_id = self._validate_manifest(mock_app['url'])

        validation_report = self._client.is_manifest_valid(manifest_validation_id)
        Assert.true(validation_report, "The manifest url is not valid.\n Validation report:\n %s" %validation_report)

        response = self._client.create(self.manifest_id)

        Assert.equal(response.status_code, 201, "Invalid status code.\n Status code received is: %s" %response.status_code)
        mock_app["app_id"] = json.loads(response.content)['id']

    def update_app_data(self, mock_app):
        # update the default app data with the custom mock app information

        data = {
            'name': mock_app['name'],
            'summary': mock_app['summary'],
            'categories': [],
            'support_email': mock_app['support_email'],
            'device_types': [],
            'payment_type': mock_app['payment_type'],
            'premium_type': 'free',
            'privacy_policy': mock_app['privacy_policy'],

            'description': mock_app['description'],
            'homepage': mock_app['homepage'],
            'support_url': mock_app['support_website']
        }

        for device in mock_app['device_type']:
            if device[1]:
                data['device_types'].append(device[0])

        available_categories = self.get_categories
        for available_category in available_categories:
            for required_category in mock_app['categories']:
                if available_category['name'] == required_category[0]:
                    data['categories'].append(available_category['id'])

        if data['device_types'] is []:
            return 'insufficient data added device_types == %s' % data['device_types']

        if len(data['categories']) < 2:
            return 'insufficient data added categories == %s' % data['categories']

        response = self._client.update(mock_app["app_id"], data)

        Assert.equal(response.status_code, 202, "Update app data failed.\n Status code %s" %response.status_code)

        # Add screenshot to app
        self.add_screenshot(mock_app)

    def add_screenshot(self, mock_app):
        response = self._client.create_screenshot(app_id=mock_app["app_id"], filename=mock_app["screenshot_link"], position=1)
        Assert.equal(response.status_code, 201,
            "Screenshot not valid.\n Status code %s\nResponse data %s" %(response.status_code, json.loads(response.content)))

    @property
    def get_categories(self):
        response = json.loads(self._client.get_categories().content)['objects']
        return response

    def delete_app(self, mock_app):
        # Not yet implemented: https://bugzilla.mozilla.org/show_bug.cgi?id=816572
        response = self._client.delete(mock_app["app_id"])
        Assert.equal(response.status_code, 204,'Delete app failed')

    def app_status(self, mock_app):
        response = self._client.status(mock_app["app_id"])
        Assert.equal(response.status_code, 200, "App status failed\n Status code: %s" %response.status_code)

        return json.loads(response.content)

    @property
    def all_apps(self):
        response = self._client.list_webapps()

        Assert.equal(response.status_code, 200, "Get all apps failed\n Status code: %s" %response.status_code)
        return json.loads(response.content)['objects']

    def change_app_status_to_pending(self, mock_app):
        self.change_app_state(mock_app, state='pending')

    def change_app_state(self, mock_app, state):
        response = self._client.app_state(app_id=mock_app["app_id"], status=state)
        Assert.equal(response.status_code, 202, "App state change failed\n Status code: %s" %response.status_code)
