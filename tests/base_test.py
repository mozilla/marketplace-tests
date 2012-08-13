#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


class BaseTest:
    """A base test class that can be extended by other tests to include utility methods."""

    def _get_resource_path(self, filename):
        """Return the path to the resources folder in the current repo."""
        import os
        path_to_resources_folder = os.path.join(os.path.split(os.path.dirname(__file__))[0], 'resources')
        return os.path.join(path_to_resources_folder, filename)

    def _delete_app(self, mozwebqa, app_name):
        from pages.desktop.developer_hub.home import Home
        dev_home = Home(mozwebqa)
        dev_home.go_to_developers_homepage()

        submitted_apps = dev_home.header.click_my_apps()

        app = submitted_apps.get_app(app_name)

        more_options_menu = app.click_more()
        manage_status = more_options_menu.click_manage_status()
        delete_popup = manage_status.click_delete_app()

        return delete_popup.delete_app()
