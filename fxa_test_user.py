#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
import os
import subprocess

from mocks.mock_user import MockUser


class FxaTestUser:
    """A base test class that can be extended by other tests to include utility methods."""

    def create_user(self):
        self.email = 'webqa-%s@restmail.net' % \
                        os.urandom(6).encode('hex')
        self.password = os.urandom(4).encode('hex')

        # Create and verify the Firefox account
        subprocess.check_call(['fxa-client', '-e', self.email,
                                '-p', self.password, 'create'])
        # Ensure to wait for an email received via restmail.
        # https://github.com/mozilla/coversheet/issues/38
        # This can be removed once the following fxa-python-client issue is fixed:
        # https://github.com/mozilla/fxa-python-client/issues/15
        time.sleep(2)
        subprocess.check_call(['fxa-client', '-e', self.email,
                                '-p', self.password, 'verify'])

        return MockUser(email=self.email, password=self.password, name=self.email.split('@')[0])
