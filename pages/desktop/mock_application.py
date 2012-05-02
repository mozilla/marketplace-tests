#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


class MockApplication(dict):

    def __init__(self, **kwargs):
        # set your default values
        import time

        current_time = time.time()
        self['name'] = 'Mock Application %s' % str(current_time).split('.')[0]
        self['url'] = 'http://marblerun.at/manifest.webapp'
        self['url_end'] = 'marble-run-%s' % str(current_time).split('.')[0]
        self['sumary'] = 'Summary of marble app %s' % str(current_time).split('.')[0]
        self['categories'] = [('Entertainment', True),
                             ('Games', True)]
        self['description'] = 'more details of marble app %s' % str(current_time).split('.')[0]
        self['privacy_policy'] = 'privacy policy of testapp %s' % str(current_time).split('.')[0]
        self['homepage'] = 'http://test.com/'
        self['support_website'] = 'http://test.com/'
        self['support_email'] = 'test@testemail.com'
        self['device_type'] = [('Desktop', True),
                              ('Mobile', False),
                              ('Tablet', False)]
        self['screenshot_link'] = 'img.jpg'
        self['payment_type'] = [('Free', True),
                               ('Premium', False),
                               ('Premium with in-app payments', False),
                               ('Free with in-app payments', False),
                               ("Premium, but I'll use my own payments system", False)]
        # update with any keyword arguments passed
        self.update(**kwargs)

    # allow getting items as if they were attributes
    def __getattr__(self, attr):
        return self[attr]

