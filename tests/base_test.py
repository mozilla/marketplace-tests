# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.desktop.consumer_pages.home import Home


class BaseTest:
    """A base test class that can be extended by other tests to include utility methods."""

    def _get_resource_path(self, filename):
        """Return the path to the resources folder in the current repo."""
        import os
        path_to_resources_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources')
        return os.path.join(path_to_resources_folder, filename)

    def _take_first_free_app_name(self, base_url, selenium):

        home_page = Home(base_url, selenium)
        home_page.go_to_homepage()

        home_page.header.search(':free')
        app_name = home_page.first_app_name
        return app_name
