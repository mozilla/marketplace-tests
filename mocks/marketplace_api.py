#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from unittestzero import Assert
from marketplace import Client
import json

DEFAULT_DOMAIN = 'marketplace-dev.allizom.org'


class MarketplaceAPI:

    def __init__(self, key, secret, domain=None):
        domain = domain or DEFAULT_DOMAIN
        self._client = Client(
            domain=domain,
            consumer_key=key,
            consumer_secret=secret)

    def submit_app(self, app):

        # validate app manifest
        self._validate_manifest(app)

        # create app
        self._create_app(app)

        # update the app with the mock app data
        self.update_app_data(app)

        # Add screenshot to app
        self.add_screenshot(app)

        # Add content ratings to app, which automatically updates the status to pending
        self.add_content_ratings(app)

    def _validate_manifest(self, app):
        response = self._client.validate_manifest(app['url'])
        manifest_validation_id = json.loads(response.content)['id']

        # validate manifest
        validation_report = self._client.is_manifest_valid(manifest_validation_id)
        Assert.true(validation_report, "The manifest url is not valid.\n Validation report:\n %s" % validation_report)
        app['manifest_validation_id'] = manifest_validation_id

    def _create_app(self, app):
        # create app using the manifest
        response = self._client.create(app.manifest_validation_id)

        Assert.equal(response.status_code, 201, "Invalid status code.\n Status code received is: %s" % response.status_code)
        app_dict = json.loads(response.content)
        app['id'] = app_dict['id']
        app['url_end'] = app_dict['slug']

    def update_app_data(self, app):
        # update the default app data with the custom mock app information

        data = {
            'name': app.name,
            'summary': app.summary,
            'categories': [],
            'support_email': app.support_email,
            'device_types': [],
            'payment_type': app.payment_type,
            'premium_type': 'free',
            'privacy_policy': app.privacy_policy,
            'description': app.description,
            'homepage': app.homepage,
            'support_url': app.support_website
        }

        # device_types: a list of the device types at least one of: 'desktop', 'android-tablet', 'android-mobile', 'firefoxos'
        data['device_types'] = [device[0] for device in app['device_type'] if device[1]]

        Assert.true(data['device_types'], 'insufficient data added device_types')

        # categories: a list of the categories, at least two of the category ids provided from the category api
        data['categories'] = [category['slug'] for category in self._categories
                              if category['name'] in [mock_category[0] for mock_category in app.categories]]

        Assert.greater_equal(len(data['categories']), 2,
                             'Insufficient data added categories == %s\n Minimum 2 categories required' % data['categories'])

        response = self._client.update(app.id, data)

        Assert.equal(response.status_code, 202, "Update app data failed.\n Status code %s" % response.status_code)

    def add_screenshot(self, app):
        response = self._client.create_screenshot(app_id=app.id, filename=app["screenshot_link"], position=1)
        Assert.equal(response.status_code, 201,
                     "Screenshot not valid.\n Status code %s\nResponse data %s" % (response.status_code,
                                                                                   json.loads(response.content)))

    def add_content_ratings(self, app):
        response = self._client.add_content_ratings(
            app_id=app.id,
            submission_id=app.submission_id,
            security_code=app.security_code)
        try:
            response_data = json.loads(response.content)
        except ValueError:
            response_data = 'Unknown'
        Assert.equal(response.status_code, 201,
                     "Content ratings not added.\n Status code %s\nResponse data %s" %
                     (response.status_code, response_data))

    @property
    def _categories(self):
        return json.loads(self._client.get_categories().content)['objects']

    def delete_app(self, app):
        response = self._client.delete(app.id)
        Assert.equal(response.status_code, 204, 'Delete app failed\n Status code: %s' % response.status_code)

    def app_status(self, app):
        response = self._client.status(app.id)
        Assert.equal(response.status_code, 200, "App status failed\n Status code: %s" % response.status_code)

        return json.loads(response.content)

    @property
    def all_apps(self):
        response = self._client.list_webapps()

        Assert.equal(response.status_code, 200, "Get all apps failed\n Status code: %s" % response.status_code)
        return json.loads(response.content)['objects']

    def change_app_status_to_pending(self, app):
        self.change_app_state(app, state='pending')

    def change_app_state(self, app, state):
        response = self._client.app_state(app_id=app.id, status=state)
        Assert.equal(response.status_code, 202, "App state change failed\n Status code: %s" % response.status_code)

    def submit_app_review(self, app_id, review, rating):
        from urlparse import urlunparse
        client = self._client
        endpoint = '/apps/rating/'
        _url = urlunparse((client.protocol, '%s:%s' % (client.domain,
                                                       client.port),
                           '%s/api/v1%s' % (client.prefix, endpoint),
                           '', '', ''))
        response = self._client.conn.fetch('POST', _url, {
            'app': app_id,
            'body': review,
            'rating': rating,
        })

        response = json.loads(response.text)
        return response['resource_uri'].split('/')[-2]

    def get_app_review(self, app_id=None, app_slug=None, user='mine'):
        if app_id is None and app_slug is None:
            raise ValueError('Provide either app_id or app_slug.')

        from urlparse import urlunparse
        client = self._client
        endpoint = '/apps/rating/?app=%s&user=%s' % (app_slug if app_slug is not None else app_id, user)
        _url = urlunparse((client.protocol, '%s:%s' % (client.domain,
                                                       client.port),
                           '%s/api/v1%s' % (client.prefix, endpoint),
                           '', '', ''))

        resp = self._client.conn.fetch('GET', _url)
        return json.loads(resp.text)

    def submit_app_review_for_either(self, apps, review, rating):
        from requests.exceptions import HTTPError
        from datetime import datetime

        # Get app details
        apps_details = {}
        for app in apps:
            apps_details.update({
                app: self.get_app(app),
            })

        # try submitting review for one app
        for app_name, app in apps_details.iteritems():
            # Submit a review using marketplace API
            try:
                review_id = self.submit_app_review(app['id'], review,
                                                   rating)
                selected_app = app_name
            except HTTPError, e:
                continue
            break

        # if none of the apps have a review, then use the review that got
        # submitted eariler
        if locals().get('review_id', None) is None:
            reviews = []

            # find app that has a review and return that
            for app_name, app in apps_details.iteritems():
                reviews.append(self.get_app_review(app['id']))

            # compare submission time of both the reviews and select the one
            # that got submitted first
            first = datetime.strptime(reviews[0]['objects'][0]['modified'],
                                      '%Y-%m-%dT%H:%M:%S')
            second = datetime.strptime(reviews[1]['objects'][0]['modified'],
                                       '%Y-%m-%dT%H:%M:%S')
            if first > second:
                selected_app = apps_details.keys()[1]
                review_id = reviews[1]['objects'][0]['resource_uri'].split('/')[-2]
            else:
                selected_app = apps_details.keys()[0]
                review_id = reviews[0]['objects'][0]['resource_uri'].split('/')[-2]

        return (selected_app, review_id)

    def delete_app_review(self, review_id):
        from urlparse import urlunparse
        client = self._client
        endpoint = '/apps/rating/%s/' % review_id
        _url = urlunparse((client.protocol, '%s:%s' % (client.domain,
                                                       client.port),
                           '%s/api/v1%s' % (client.prefix, endpoint),
                           '', '', ''))
        return self._client.conn.fetch('DELETE', _url)

    def get_app(self, app):
        response = self._client.conn.fetch('GET', self._client.url('app') % app)
        response = json.loads(response.text)
        return response
