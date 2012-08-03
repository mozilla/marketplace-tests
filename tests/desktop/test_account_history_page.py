#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest

from unittestzero import Assert

from pages.desktop.consumer_pages.home import Home


class TestAccountHistory:

    @pytest.mark.nondestructive
    def test_that_verifies_account_history_page(self, mozwebqa):
        '''https://www.pivotaltracker.com/projects/477093#!/stories/31914365'''

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.true(home_page.is_the_current_page)

        home_page.login(user = "default")

        acc_history_page = home_page.footer.click_account_history()

        # Check top page title
        Assert.equal("Account History", acc_history_page.account_history_title)

        # Check sort by section
        Assert.true(acc_history_page.is_sort_by_item_visible)
        Assert.equal("Sort by:", acc_history_page.sort_text)

        Assert.true(acc_history_page.is_purchased_date_text_visible)
        Assert.equal("Purchase Date", acc_history_page.purchased_date_text)
        Assert.equal("Purchase Date", acc_history_page.element_selected)

        Assert.true(acc_history_page.is_price_item_visible)
        Assert.equal("Price", acc_history_page.price_item_text)

        Assert.true(acc_history_page.is_name_item_visible)
        Assert.equal("Name", acc_history_page.name_item_text)

        # Check application boxes
        for element in acc_history_page.purchased_apps:
            Assert.true(element.is_application_icon_visible)
            Assert.true(element.is_application_name_visible)
            Assert.true(element.is_application_description_visible)
            Assert.true(element.is_application_price_visible)
            Assert.true(element.is_application_categories_section_visible)
            Assert.true(element.is_application_rating_section_visible)
            Assert.true(element.is_application_weekly_downloads_section_visible)

            if element.application_price_text == "FREE":
                continue
            else:
                Assert.true(element.is_premium_application_purchased_date_visible)
                Assert.true(element.is_premium_application_support_link_visible)

        Assert.less(acc_history_page.purchased_applications_count, 20)
