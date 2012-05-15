#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


class MockApplication(dict):

    def __init__(self, **kwargs):
        # set your default values
        import time

        current_time = str(time.time()).split('.')[0]
        self['name'] = 'Mock Application %s' % current_time
        self['url'] = 'http://%s.testmanifest.com/manifest.webapp' % current_time
        self['url_end'] = 'marble-run-%s' % current_time
        self['summary'] = 'Summary of marble app %s' % current_time
        self['categories'] = [('Entertainment', True),
                             ('Games', True)]
        self['description'] = 'more details of marble app %s' % current_time
        self['privacy_policy'] = 'privacy policy of testapp %s' % current_time
        self['homepage'] = 'http://test.com/'
        self['support_website'] = 'http://test.com/'
        self['support_email'] = 'test@testemail.com'
        self['device_type'] = [('Desktop', True),
                              ('Mobile', False),
                              ('Tablet', False)]

        self['screenshot_link'] = self._get_resource_path('img.jpg')
        self['payment_type'] = 'Free'

        # update with any keyword arguments passed
        self.update(**kwargs)

    # allow getting items as if they were attributes
    def __getattr__(self, attr):
        return self[attr]

    def _get_resource_path(self, filename):
        """returns the path to the resources folder in the current repo"""
        import os
        path_to_resources_folder = os.path.join(os.path.split(os.path.dirname(__file__))[0], 'resources')
        return os.path.join(path_to_resources_folder, filename)
