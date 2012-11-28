#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marketplace import Client
import json

MARKETPLACE_DOMAIN = 'marketplace-dev.allizom.org'

class MarketplaceApp:
    app_id = None
    manifest_id = None

    def __init__(self, mock_app, user= None):

        if user:
            self._client = Client(domain=MARKETPLACE_DOMAIN, consumer_key = user['consumer_key'], consumer_secret = user['consumer_secret'])
        else:
            self._client = Client(domain=MARKETPLACE_DOMAIN)

        self.mock_app = mock_app


    def validate_manifest(self):
        response = self._client.validate_manifest(self.mock_app['url'])
        self.manifest_id = json.loads(response.content)['id']

    def submit_app(self):
        if self._client.is_manifest_valid(self.manifest_id) is True:
            response = self._client.create(self.manifest_id)
            if response.status_code == 201:
                self.app_id = json.loads(response.content)['id']
                return self.app_id
            else:
                return response.status_code

    def update(self):
        data={
            'name': self.mock_app['name'],
            'summary': self.mock_app['summary'],
            'categories':[],
            'support_email': self.mock_app['support_email'],
            'device_types': ['desktop'],
            'payment_type': self.mock_app['payment_type'],
            'privacy_policy': self.mock_app['privacy_policy'],

            'description': self.mock_app['description'],
            'homepage' : self.mock_app['homepage'],
            'support_url': self.mock_app['support_website']
        }

#        for device in self.mock_app['device_type']:
#            if device[1]:
#                data['device_types'].append(device[0])

        available_categories = self.get_categories
        for available_category in available_categories:
            for required_category in self.mock_app['categories']:
                if available_category['name'] == required_category[0]:
                    data['categories'].append(available_category['id'])

        if data['device_types'] is []:
            return 'insufficient data added device_types == %s' %data['device_types']

        if len(data['categories']) < 2:
            return 'insufficient data added categories == %s' %data['categories']

        response = self._client.update(self.app_id, data)

        if response.status_code == 202:
            return True


    def add_screenshot(self):
        response = self._client.create_screenshot(app_id=self.app_id, filename=self.mock_app["screenshot_link"], position=1)
        if response.status_code == 201:
            return json.loads(response.content)

    @property
    def get_categories(self):
        response = json.loads(self._client.get_categories().content)['objects']
        return response

    def delete(self):
        response = self._client.delete(self.app_id)
        if response.status_code == 204:
            return True

    @property
    def get_app_status(self):
        response = self._client.status(self.app_id)
        if response.status_code == 200:
            return json.loads(response.content)


