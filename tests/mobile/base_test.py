#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from unittestzero import Assert


class BaseTest:
    """A base test class that can be extended by other tests to include utility methods."""

    def search(self, page_obj, search_term):
        page_obj.header.click_search()
        Assert.true(page_obj.header.is_search_visible)
        page_obj.header.type_in_search_field(search_term)
        page_obj.header.submit_search()
        from pages.mobile.search import Search
        return Search(page_obj.testsetup)
