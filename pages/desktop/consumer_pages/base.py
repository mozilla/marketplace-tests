# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException

from pages.page import Page, PageRegion
import expected


class Base(Page):

    _notification_locator = (By.ID, 'notification')
    _notification_content_locator = (By.ID, 'notification-content')
    _search_locator = (By.ID, 'search-q')

    @property
    def page_title(self):
        WebDriverWait(self.selenium, 10).until(lambda s: self.selenium.title)
        return self.selenium.title

    def wait_for_page_to_load(self):
        WebDriverWait(self.selenium, self.timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'body.loaded')))

    def link_destination(self, locator):
        link = self.selenium.find_element(*locator)
        return link.get_attribute('href')

    def wait_for_notification(self, message=None):
        WebDriverWait(self.selenium, self.timeout).until(
            EC.visibility_of_element_located(
                self._notification_locator))
        if message is not None:
            WebDriverWait(self.selenium, self.timeout).until(
                EC.text_to_be_present_in_element(
                    self._notification_content_locator, message))

    def go_to_debug_page(self):
        self.header.search(':debug')
        from pages.desktop.regions.debug import Debug
        return Debug(self.testsetup)

    def set_region(self, region):
        debug_page = self.go_to_debug_page()
        debug_page.select_region(region)
        self.wait_for_notification()

    def login(self, email, password):
        from fxapom.pages.sign_in import SignIn
        fxa_login = SignIn(self.testsetup)
        fxa_login.sign_in(email, password)
        self.wait_for_notification()

    @property
    def header(self):
        return self.HeaderRegion(self.testsetup)

    @property
    def footer(self):
        return self.FooterRegion(self.testsetup)

    class HeaderRegion(Page):

        _categories_header_locator = (By.CLASS_NAME, 'app-categories')
        _categories_toggle_locator = (By.CLASS_NAME, 'nav-category-link')
        _categories_locator = (By.CSS_SELECTOR, '.app-categories li:not(.cat-menu-all)')
        _search_toggle_locator = (By.CLASS_NAME, 'search-btn-desktop')
        _search_input_locator = (By.ID, 'search-q-desktop')
        _search_input_placeholder_locator = (By.CSS_SELECTOR, '.header-child--input-placeholder')
        _suggestion_list_title_locator = (By.CSS_SELECTOR, '#site-search-suggestions .wrap > p > a > span')
        _search_suggestions_locator = (By.CSS_SELECTOR, '#site-search-suggestions')
        _search_suggestions_list_locator = (By.CSS_SELECTOR, '#site-search-suggestions > ul > li')
        _site_logo_locator = (By.CSS_SELECTOR, '#navigation .site > a')
        _settings_toggle_locator = (By.CLASS_NAME, 'mkt-settings-btn')
        _settings_menu_locator = (By.CLASS_NAME, 'settings-menu-desktop')
        _settings_menu_item_locator = (By.CSS_SELECTOR, '.settings-menu-desktop a[href*="settings"]')
        _my_apps_menu_locator = (By.CSS_SELECTOR, '.settings-menu-desktop a[href*="purchases"]')
        _sign_out_locator = (By.CLASS_NAME, 'logout')
        _sign_in_locator = (By.CSS_SELECTOR, '.nav--settings--logged-out.persona:not(.register)')

        @property
        def is_user_logged_in(self):
            return self.is_element_visible(*self._settings_toggle_locator)

        @property
        def categories_name(self):
            return self.selenium.find_element(*self._categories_toggle_locator).text

        def open_categories_menu(self):
            categories = self.selenium.find_element(*self._categories_header_locator)
            self.selenium.find_element(*self._categories_toggle_locator).click()
            WebDriverWait(self.selenium, self.timeout).until(expected.element_not_moving(categories))

        @property
        def categories(self):
            categories = self.selenium.find_elements(*self._categories_locator)
            return [self.Category(self.testsetup, element) for element in categories]

        def open_settings_menu(self):
            settings_menu = self.selenium.find_element(*self._settings_menu_locator)
            if 'active' not in settings_menu.get_attribute('class'):
                self.selenium.find_element(*self._settings_toggle_locator).click()
                WebDriverWait(self.selenium, self.timeout).until(expected.element_not_moving(settings_menu))

        def click_sign_in(self):
            self.wait_for_element_visible(*self._sign_in_locator)
            self.selenium.find_element(*self._sign_in_locator).click()

        def click_sign_out(self):
            self.open_settings_menu()
            self.selenium.find_element(*self._sign_out_locator).click()
            WebDriverWait(self.selenium, self.timeout, ignored_exceptions=StaleElementReferenceException).\
                until(lambda s: self.is_element_visible(*self._sign_in_locator))

        def click_edit_account_settings(self):
            self.open_settings_menu()
            self.selenium.find_element(*self._settings_menu_item_locator).click()
            from pages.desktop.consumer_pages.account_settings import BasicInfo
            return BasicInfo(self.testsetup)

        def click_my_apps(self):
            self.open_settings_menu()
            self.selenium.find_element(*self._my_apps_menu_locator).click()
            from pages.desktop.consumer_pages.account_settings import My_Apps
            return My_Apps(self.testsetup)

        def search(self, search_term):
            """
            Searches for an app using the available search field
            :Args:
             - search_term - string value of the search field
            """
            search_toggle = self.selenium.find_element(*self._search_toggle_locator)
            WebDriverWait(self.selenium, self.timeout).until(EC.visibility_of(search_toggle))
            search_toggle.click()
            search_field = self.selenium.find_element(*self._search_input_locator)
            WebDriverWait(self.selenium, self.timeout).until(EC.visibility_of(search_field))
            search_field.send_keys(search_term)
            search_field.submit()
            from pages.desktop.consumer_pages.search import Search
            return Search(self.testsetup, search_term)

        def search_and_click_on_app(self, search_term):

            search_page = self.search(search_term)

            # Select the application link in the list
            # It can't always be the first in the list
            results = search_page.results
            for i in range(len(results)):
                if search_term == results[i].name:
                    return results[i].click_name()
            raise Exception('No application named %s could be found.' % search_term)

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
            self.selenium.find_element(*self._search_toggle_locator).click()
            return self.selenium.find_element(*self._search_input_placeholder_locator).text

        @property
        def is_logo_visible(self):
            return self.is_element_visible(*self._site_logo_locator)

        @property
        def is_search_visible(self):
            return self.is_element_visible(*self._search_toggle_locator)

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

        class Category(PageRegion):

            _link_locator = (By.TAG_NAME, 'a')

            @property
            def name(self):
                return self.find_element(*self._link_locator).text

            def click(self):
                name = self.name
                self.find_element(*self._link_locator).click()
                from pages.desktop.consumer_pages.category import Category
                return Category(self.testsetup, name)

    class FooterRegion(Page):

        _region_link_locator = (By.CSS_SELECTOR, '.region')
        _develop_apps_button_locator = (By.CSS_SELECTOR, '.button.devhub')
        _developer_hub_link_locator = (By.CSS_SELECTOR, '.footer-support-navigation a[href="/developers/"]')
        _submit_feedback_link_locator = (By.CSS_SELECTOR, '.group.links .submit-feedback')
        _my_submissions_link_locator = (By.CSS_SELECTOR, '.footer-support-navigation a[href*="/submissions"]')
        _privacy_policy_link_locator = (By.CSS_SELECTOR, '#footer a[href*="privacy-policy"]')
        _term_of_use_link_locator = (By.CSS_SELECTOR, '#footer a[href*="terms-of-use"]')
        _support_link_locator = (By.CSS_SELECTOR, '.footer-support-navigation a[href*="/support"]')
        _report_abuse_link_locator = (By.CSS_SELECTOR, '#footer a[href*="fraud-report"]')
        _feedback_link_locator = (By.CSS_SELECTOR, '.footer-support-navigation .submit-feedback')

        footer_links_list = [
            {
                'locator': (By.CSS_SELECTOR, '.footzilla > a'),
                'url_suffix': 'mozilla.org/',
            }, {
                'locator': (By.CSS_SELECTOR, '#footer > .footer-content > p > a:nth-child(1)'),
                'url_suffix': '/about/legal.html#site',
            }, {
                'locator': (By.CSS_SELECTOR, '#footer > .footer-content > p > a:nth-child(2)'),
                'url_suffix': 'creativecommons.org/licenses/by-sa/3.0/',
            }, {
                'locator': _privacy_policy_link_locator,
                'url_suffix': '/privacy-policy',
            }, {
                'locator': _term_of_use_link_locator,
                'url_suffix': '/terms-of-use',
            }, {
                'locator': _report_abuse_link_locator,
                'url_suffix': '/legal/fraud-report/index.html',
            }, {
                'locator': _developer_hub_link_locator,
                'url_suffix': '/developers/',
            }, {
                'locator': _my_submissions_link_locator,
                'url_suffix': '/developers/submissions',
            }, {
                'locator': _support_link_locator,
                'url_suffix': '/marketplace-apps-firefox-desktop',
            }, {
                'locator': _feedback_link_locator,
                'url_suffix': '/#',
            }
        ]
