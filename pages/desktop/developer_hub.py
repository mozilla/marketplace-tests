#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from pages.desktop.base import Base
from datetime import datetime


class DeveloperHub(Base):
    #Developer Hub homepage
    #https://marketplace-dev.allizom.org/developers/
    _page_title = "Developer Hub | Mozilla Marketplace"

    _submit_app = (By.CSS_SELECTOR, '.button.prominent')

    def go_to_developer_hub(self):
        self.selenium.get('%s/developers/' % self.base_url)

    def generate_test_app(self, name='Marble app', url='http://marblerun.at/manifest.webapp', url_end='marble-run', sumary='Summary of marble app',
                          categories=[{'name':'Entertainment', 'value':True}, {'name':'Games', 'value':True}],
                          description='more details of marble app', privacy_policy='privacy policy of testapp',
                          homepage='http://marblerun.at/', support_website='http://marblerun.at/', support_email='test@testemail.com',
                          device_type=[{'name':'Desktop', 'value':True}, {'name':'Mobile', 'value':True}, {'name':'Tablet', 'value':True}],
                          screenshot_link='img.jpg', payment_type=[{'name':'Free', 'value':True}, {'name':'Premium', 'value':False},
                          {'name':'Premium with in-app payments', 'value':False}, {'name':'Free with in-app payments', 'value':False},
                          {'name':"Premium, but I'll use my own payments system", 'value':False}]):

        dt_string = datetime.utcnow().isoformat()
        app = {}
        app['name'] = u'%(name)s %(dt_string)s' % {'name': name, 'dt_string': dt_string}
        app['url'] = u'%(url)s' % {'url': url}
        app['url_end'] = u'%(url_end)s_%(dt_string)s' % {'url_end': url_end, 'dt_string': dt_string.replace(':', '-')}
        app['sumary'] = u'%(sumary)s %(dt_string)s' % {'sumary': sumary, 'dt_string': dt_string}
        app['categories'] = categories
        app['description'] = u'%(description)s %(dt_string)s' % {'description': description, 'dt_string': dt_string}
        app['privacy_policy'] = u'%(privacy_policy)s %(dt_string)s' % {'privacy_policy': privacy_policy, 'dt_string': dt_string}
        app['homepage'] = u'%(homepage)s' % {'homepage': homepage}
        app['support_website'] = u'%(support_website)s' % {'support_website': support_website}
        app['support_email'] = u'%(support_email)s' % {'support_email': support_email}
        app['device_type'] = device_type
        app['screenshot_link'] = u'%(file)s' % {'file': screenshot_link}
        app['payment_type'] = payment_type

        return app
