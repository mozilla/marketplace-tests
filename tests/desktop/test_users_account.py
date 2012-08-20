#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from pages.desktop.consumer_pages.home import Home
from pages.desktop.paypal.paypal import PayPal
from mocks.mock_user import MockUser


class TestAccounts:

    def test_create_new_user(self, mozwebqa):
        user = MockUser()
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        home_page.create_new_user(user)
        home_page.login(user)

        Assert.true(home_page.is_the_current_page)
        Assert.true(home_page.footer.is_user_logged_in)

    @pytest.mark.nondestructive
    def test_user_can_login_and_logout_using_browser_id_in_consumer_pages(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        home_page.login(user="default")

        Assert.true(home_page.is_the_current_page)
        Assert.true(home_page.footer.is_user_logged_in)

        home_page.footer.click_logout()
        Assert.false(home_page.footer.is_user_logged_in)

    def _payment_settings_page_as_user(self, mozwebqa, user):
        # Now we start to test the marketplace pages
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        home_page.login(user=user)

        Assert.true(home_page.is_the_current_page)
        Assert.true(home_page.footer.is_user_logged_in)

        # go to Payment Settings page
        settings_page = home_page.footer.click_account_settings()
        Assert.true(settings_page.is_the_current_page)

        payment_settings_page = settings_page.click_payment_menu()
        Assert.equal('Payment Settings', payment_settings_page.header_title)
        return payment_settings_page

    @pytest.mark.nondestructive
    def test_editing_user_profile(self, mozwebqa):
        """Test for https://www.pivotaltracker.com/story/show/33709085"""
        
        user = MockUser()
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        home_page.create_new_user(user)
        home_page.login(user)

        profile_page = home_page.footer.click_account_settings()
        _username = user['email'].split('@')[0]

        #Initial check
        Assert.equal(profile_page.browser_id_email, user['email'])
        Assert.equal(profile_page.username, _username)
        Assert.equal(profile_page.display_name, _username)

        #Data to submit. Username and Bio should be unique 
        name = 'Napoleon'
        username = _username[::-1]
        location = 'Saint Helena'
        occupation = 'Emperor of the French'
        homepage = 'https://mozilla.org/'
        bio = 'Unique bio for %s' % _username

        profile_page.edit_display_name(name)
        profile_page.edit_username(username)
        profile_page.edit_location(location)
        profile_page.edit_occupation(occupation)
        profile_page.edit_homepage(homepage)
        profile_page.edit_bio(bio)
        profile_page.check_email_me_checkbox()
        profile_page.save_changes()

        Assert.equal(profile_page.notification_text, 'Profile Updated')
        Assert.equal(profile_page.display_name, name)
        Assert.equal(profile_page.username, username)
        Assert.equal(profile_page.location, location)
        Assert.equal(profile_page.occupation, occupation)
        Assert.equal(profile_page.homepage, homepage)
        Assert.equal(profile_page.bio, bio)
        Assert.false(profile_page.is_email_me_checked)
