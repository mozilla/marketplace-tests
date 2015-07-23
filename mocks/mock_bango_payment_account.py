# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time


class MockBangoPaymentAccount(dict):

    def __init__(self, **kwargs):

        current_time = str(time.time()).split('.')[0]
        self['bank_account_holder_name'] = 'bankAccountPayeeName %s' % current_time
        self['bank_account_number'] = current_time
        self['bank_account_code'] = current_time
        self['address'] = 'address1 %s' % current_time
        self['city'] = 'addressCity %s' % current_time
        self['state'] = 'addressState %s' % current_time
        self['zip_code'] = current_time
        self['phone'] = 'addressPhone %s' % current_time
        self['bank_name'] = 'bankName %s' % current_time
        self['bank_address'] = 'bankAddress1 %s' % current_time
        self['bank_zip_code'] = current_time
        self['company_name'] = 'companyName %s' % current_time
        self['vendor_name'] = 'vendorName %s' % current_time
        self['finance_email'] = 'finance@%s.com' % current_time
        self['admin_email'] = 'admin@%s.com' % current_time
        self['support_email'] = 'support@%s.com' % current_time
        self['account_name'] = 'account_name %s' % current_time

        # update with any keyword arguments passed
        self.update(**kwargs)

    # allow getting items as if they were attributes
    def __getattr__(self, attr):
        return self[attr]
