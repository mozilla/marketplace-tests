#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException

from pages.page import Page


class Base(Page):


    _load_page_details_baloon_locator = (By.CSS_SELECTOR, '.loading')
    _notification_locator = (By.ID, 'notification')
    _notification_content_locator = (By.ID, 'notification-content')
    _search_locator = (By.ID, 'search-q')

    @property
    def page_title(self):
        WebDriverWait(self.selenium, 10).until(lambda s: self.selenium.title)
        return self.selenium.title

    def wait_for_page_to_load(self):
        self.wait_for_element_not_present(*self._load_page_details_baloon_locator)

    def scroll_to_element(self, *locator):
        """Scroll to element"""
        el = self.selenium.find_element(*locator)
        self.selenium.execute_script("window.scrollTo(0, %s)" % (el.location['y'] + el.size['height']))

    def link_destination(self, locator):
        link = self.selenium.find_element(*locator)
        return link.get_attribute('href')

    @property
    def notification_visible(self):
        return self.is_element_visible(*self._notification_locator)

    @property
    def notification_message(self):
        return self.selenium.find_element(*self._notification_content_locator).text

    def wait_notification_box_visible(self):
        self.wait_for_element_visible(*self._notification_locator)

    def wait_notification_box_not_visible(self):
        self.wait_for_element_not_visible(*self._notification_locator)

    def go_to_debug_page(self):

        search_field = self.selenium.find_element(*self._search_locator)
        search_field.send_keys(":debug")
        search_field.submit()
        from pages.desktop.regions.debug import Debug
        return Debug(self.testsetup)

    def set_region(self, region):

        debug_page = self.go_to_debug_page()
        debug_page.select_region(region)

        self.wait_notification_box_visible()
        if not self.notification_visible:
            raise Exception('Unable to change region to %s. Notification not displayed'
                            % (region))

        self.wait_notification_box_not_visible()

    def login(self, user=None):
        from pages.fxa import FirefoxAccounts
        fxa = FirefoxAccounts(self.testsetup)
        fxa.login_user(user)
        self.wait_notification_box_visible()
        self.wait_notification_box_not_visible()

    @property
    def header(self):
        return self.HeaderRegion(self.testsetup)

    @property
    def footer(self):
        return self.FooterRegion(self.testsetup)


    class HeaderRegion(Page):

        _search_locator = (By.ID, 'search-q')
        _login_locator = (By.CSS_SELECTOR, '.header-button.persona')
        _suggestion_list_title_locator = (By.CSS_SELECTOR, '#site-search-suggestions .wrap > p > a > span')
        _search_suggestions_locator = (By.CSS_SELECTOR, '#site-search-suggestions')
        _search_suggestions_list_locator = (By.CSS_SELECTOR, '#site-search-suggestions > ul > li')
        _site_logo_locator = (By.CSS_SELECTOR, '.site > a')
        _account_settings_locator = (By.CSS_SELECTOR, '.header-button.settings')
        _edit_user_settings_locator = (By.CSS_SELECTOR, '.account-links.only-logged-in > ul > li > a')
        _sign_out_locator = (By.CSS_SELECTOR, '.logout')
        _sign_in_locator = (By.CSS_SELECTOR, '.header-button.persona')

        @property
        def is_user_logged_in(self):
            return self.is_element_visible(*self._account_settings_locator)

        def hover_over_settings_menu(self):
            hover_element = self.selenium.find_element(*self._account_settings_locator)
            ActionChains(self.selenium).\
                move_to_element(hover_element).\
                perform()

        def click_sign_in(self):
            self.wait_for_element_visible(*self._login_locator)
            self.selenium.find_element(*self._login_locator).click()

        def click_sign_out(self):
            self.hover_over_settings_menu()
            self.selenium.find_element(*self._sign_out_locator).click()
            WebDriverWait(self.selenium, self.timeout, ignored_exceptions=StaleElementReferenceException).\
                until(lambda s: self.is_element_visible(*self._sign_in_locator))

        def click_edit_account_settings(self):
            self.hover_over_settings_menu()
            self.selenium.find_element(*self._edit_user_settings_locator).click()
            from pages.desktop.consumer_pages.account_settings import BasicInfo
            return BasicInfo(self.testsetup)

        def search(self, search_term):
            """
            Searches for an app using the available search field
            :Args:

             - search_term - string value of the search field
            """
            search_field = self.selenium.find_element(*self._search_locator)
            search_field.send_keys(search_term)
            search_field.submit()
            from pages.desktop.consumer_pages.search import Search
            return Search(self.testsetup, search_term)

        def search_and_click_on_app(self, search_term):

            search_page = self.search(search_term)

            # Select the application link in the list
            # It can't always be the first in the list
            for i in range(len(search_page.results)):
                if search_term == search_page.results[i].name:
                    return search_page.results[i].click_name()

        def type_search_term_in_search_field(self, search_term):
            search_field = self.selenium.find_element(*self._search_locator)
            search_field.send_keys(search_term)
            WebDriverWait(self.selenium, self.timeout).until(lambda s: self.is_element_visible(*self._search_suggestions_locator))

        @property
        def search_suggestions(self):
            return [self.SearchSuggestion(self.testsetup, web_element)
                for web_element in self.selenium.find_elements(*self._search_suggestions_list_locator)]

        @property
        def is_search_suggestion_list_visible(self):
            return self.is_element_visible(*self._search_suggestions_locator)

        @property
        def search_suggestion_title(self):
            return self.selenium.find_element(*self._suggestion_list_title_locator).text

        @property
        def search_field_placeholder(self):
            return self.selenium.find_element(*self._search_locator).get_attribute('placeholder')

        @property
        def is_logo_visible(self):
            return self.is_element_visible(*self._site_logo_locator)

        @property
        def is_search_visible(self):
            return self.is_element_visible(*self._search_locator)

        @property
        def is_sign_in_visible(self):
            return self.is_element_visible(*self._sign_in_locator)

        class SearchSuggestion(Page):

            _app_name_locator = (By.CSS_SELECTOR, 'a > span')

            def __init__(self, testsetup, element):
                Page.__init__(self, testsetup)
                self._root_element = element

            @property
            def app_name(self):
                return self._root_element.find_element(*self._app_name_locator).text

        @property
        def menu(self):
            return self.Menu(self.testsetup)


    class FooterRegion(Page):

        _region_link_locator = (By.CSS_SELECTOR, '.region')
        _develop_apps_button_locator = (By.CSS_SELECTOR, '.button.devhub')
        _developer_hub_link_locator = (By.CSS_SELECTOR, '.group.links > a[href="/developers/"]')
        _submit_feedback_link_locator = (By.CSS_SELECTOR, '.group.links .submit-feedback')
        _my_apps_link_locator = (By.CSS_SELECTOR, '.group.links > a[href*="purchases"]')
        _my_submissions_link_locator = (By.CSS_SELECTOR, '.group.links > a[href*="submissions"]')
        _privacy_policy_link_locator = (By.CSS_SELECTOR, '#footer a[href*="privacy-policy"]')
        _term_of_use_link_locator = (By.CSS_SELECTOR, '#footer a[href*="terms-of-use"]')
        _report_abuse_link_locator = (By.CSS_SELECTOR, '#footer a[href*="fraud-report"]')

        footer_links_list = [
            {
                'locator': (By.CSS_SELECTOR, '#footzilla > a'),
                'url_suffix': 'mozilla.org/',

            }, {
                'locator': (By.CSS_SELECTOR, '#footer > .pad > p > a:nth-child(1)'),
                'url_suffix': '/about/legal.html#site',
            }, {
                'locator': (By.CSS_SELECTOR, '#footer > .pad > p > a:nth-child(2)'),
                'url_suffix': 'creativecommons.org/licenses/by-sa/3.0/',
            }, {
                'locator': (By.CSS_SELECTOR, '#footer > .pad > ul > li:nth-child(1) > a'),
                'url_suffix': '/privacy-policy',
            }, {
                'locator': (By.CSS_SELECTOR, '#footer > .pad > ul > li:nth-child(2) > a'),
                'url_suffix': '/terms-of-use',
            }, {
                'locator': (By.CSS_SELECTOR, '#footer > .pad > ul > li:nth-child(3) > a'),
                'url_suffix': '/legal/fraud-report/index.html',
            }, {
                'locator': (By.CSS_SELECTOR, 'div:nth-child(2).group.links > a:nth-child(1)'),
                'url_suffix': '/developers/',
            }, {
                'locator': (By.CSS_SELECTOR, 'div:nth-child(3).group.links > a:nth-child(1)'),
                'url_suffix': '/settings',
            }, {
                'locator': (By.CSS_SELECTOR, 'div:nth-child(3).group.links > a:nth-child(2)'),
                'url_suffix': '/purchases',
            }, {
                'locator': (By.CSS_SELECTOR, 'div:nth-child(3).group.links > a:nth-child(3)'),
                'url_suffix': '/developers/submissions',
            }
        ]

        @property
        def is_develop_apps_button_visible(self):
            return self.is_element_visible(*self._develop_apps_button_locator)

        @property
        def is_developer_hub_link_visible(self):
            return self.is_element_visible(*self._developer_hub_link_locator)

        @property
        def is_feedback_link_visible(self):
            return self.is_element_visible(*self._submit_feedback_link_locator)

        @property
        def is_region_link_visible(self):
            return self.is_element_visible(*self._region_link_locator)

        @property
        def is_my_apps_link_visible(self):
            return self.is_element_visible(*self._my_apps_link_locator)

        @property
        def is_my_submissions_link_visible(self):
            return self.is_element_visible(*self._my_submissions_link_locator)

        @property
        def is_privacy_link_visible(self):
            return self.is_element_visible(*self._privacy_policy_link_locator)

        @property
        def is_terms_link_visible(self):
            return self.is_element_visible(*self._term_of_use_link_locator)

        @property
        def is_report_abuse_link_visible(self):
            return self.is_element_visible(*self._report_abuse_link_locator)
