#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from unittestzero import Assert

from pages.desktop.developer_hub import DeveloperHub


class TestDeveloperHub:

    @pytest.mark.nondestructive
    def test_that_checks_apps_are_sorted_by_name(self, mozwebqa):
        dev_hub = DeveloperHub(mozwebqa)
        dev_hub.go_to_developer_hub()
        dev_hub.login()

        dev_hub.sorter.sort_by('Name')

        submited_app_names = [app.name for app in dev_hub.submited_apps]
        Assert.is_sorted_ascending(submited_app_names, 'Apps are not sorted ascending.\nApp names = %s' % submited_app_names)

    @pytest.mark.nondestructive
    def test_that_checks_apps_are_sorted_by_date(self, mozwebqa):
        dev_hub = DeveloperHub(mozwebqa)
        dev_hub.go_to_developer_hub()
        dev_hub.login()

        dev_hub.sorter.sort_by('Created')

        submited_app_dates = [app.date for app in dev_hub.submited_apps_completed]
        Assert.is_sorted_ascending(submited_app_dates, 'Apps are not sorted ascending.\nApp dates = %s' % submited_app_dates)
