#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


class MockReview(dict):

    def __init__(self, **kwargs):
        # set your default values
        import time
        current_time = str(time.time()).split('.')[0]
        import random
        self['rating'] = random.randint(1, 5)
        self['body'] = 'automatic app review by Selenium tests %s' % current_time

        # update with any keyword arguments passed
        self.update(**kwargs)

    # allow getting items as if they were attributes
    def __getattr__(self, attr):
        return self[attr]
