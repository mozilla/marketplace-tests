#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


class MockApplication(dict):

    def __init__(self, **kwargs):
        # set your default values
        import time

        current_time = str(time.time()).split('.')[0]
        self['app_type'] = 'hosted'
        self['name'] = 'Mock Application %s' % current_time
        self['url_end'] = 'marble-run-%s' % current_time
        self['summary'] = 'Summary of marble app %s' % current_time
        self['categories'] = [('Entertainment', True),
                             ('Games', True)]
        self['description'] = 'more details of marble app %s' % current_time
        self['privacy_policy'] = 'privacy policy of testapp %s' % current_time
        self['homepage'] = 'http://test%s.com/' % current_time
        self['support_website'] = 'http://test%s.com/' % current_time
        self['support_email'] = 'test%s@testemail.com' % current_time
        self['device_type'] = [('firefoxos', True),
                              ('desktop', False),
                              ('android-mobile', False),
                              ('android-tablet', False)]

        self['screenshot_link'] = self._get_resource_path('img.jpg')
        self['payment_type'] = 'free'
        self['app_price'] = 'Tier 1 - $0.99'
        self['make_public'] = True
        self['upsell'] = False
        self['free_app'] = ''
        self['pitch_app'] = ''
        self['business_account'] = 'Yes'
        self['first_name'] = 'Marketplace'
        self['last_name'] = 'test'
        self['address'] = '1 Main St'
        self['city'] = 'San Jose'
        self['state'] = 'CA'
        self['post_code'] = '95131'
        self['country'] = 'US'
        self['phone'] = '4086780945'

        # update with any keyword arguments passed
        self.update(**kwargs)

        if self['app_type'] == 'packaged':
            self['app_path'] = self._get_resource_path('app.zip')
            import urllib
            response = urllib.urlopen('http://testpackagedapp.appspot.com/build')
            app = response.read()
            zip_app = open(self['app_path'], 'wb')
            zip_app.write(app)
            zip_app.close()
        else:
            self['url'] = 'http://%s.testmanifest.com/manifest.webapp' % current_time

    # allow getting items as if they were attributes
    def __getattr__(self, attr):
        return self[attr]

    def _get_resource_path(self, filename):
        """returns the path to the resources folder in the current repo"""
        import os
        path_to_resources_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources')
        return os.path.join(path_to_resources_folder, filename)
