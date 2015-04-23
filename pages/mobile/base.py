#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from mocks.mock_user import MockUser

from pages.page import Page
from pages.page import PageRegion


class Base(Page):

    _body_class_locator = (By.CSS_SELECTOR, '#container > #page')
    _notification_locator = (By.ID, 'notification')
    _notification_content_locator = (By.ID, 'notification-content')
    _new_popular_apps_list_locator = (By.CSS_SELECTOR, '.app-list li')
    _feed_title_locator = (By.CSS_SELECTOR, '.subheader > h1')

    def set_window_size(self):
        # This method can be called to force the browser to a mobile screen
        # size which will allow you to run the mobile tests on a desktop
        # browser and reasonably emulate a mobile device
        #
        # Just add a call to page.set_window_size() in your test
        self.selenium.set_window_size(480, 800)

    @property
    def page_title(self):
        WebDriverWait(self.selenium, 10).until(lambda s: self.selenium.title)
        return self.selenium.title

    @property
    def feed_title_text(self):
        return self.find_element(*self._feed_title_locator).text

    @property
    def notification_message(self):
        return self.selenium.find_element(*self._notification_content_locator).text

    def wait_notification_box_visible(self):
        self.wait_for_element_visible(*self._notification_locator)

    def wait_notification_box_not_visible(self):
        self.wait_for_element_not_visible(*self._notification_locator)

    def login(self, user):
        credentials = (user, MockUser) and user
        from fxapom.pages.sign_in import SignIn
        fxa_login = SignIn(self.testsetup)
        fxa_login.sign_in(credentials['email'], credentials['password'])
        self.wait_notification_box_visible()
        self.wait_notification_box_not_visible()

    @property
    def header(self):
        return Header(self.testsetup)

    @property
    def nav_menu(self):
        return NavMenu(self.testsetup)

    @property
    def popular_apps(self):
        return [self.Application(self.testsetup, web_element)
                for web_element in self.selenium.find_elements(*self._new_popular_apps_list_locator)]

    @property
    def new_apps(self):
        return [self.Application(self.testsetup, web_element)
                for web_element in self.selenium.find_elements(*self._new_popular_apps_list_locator)]

    def go_to_first_free_app_page(self):
        results_page = self.header.search(':free')
        return results_page.results()[0].click()

    class Application(PageRegion):

            _link_locator = (By.CSS_SELECTOR, 'a.mkt-tile')
            _name_locator = (By.CSS_SELECTOR, '.info h3')
            _price_locator = (By.CSS_SELECTOR, '.info button.product')

            @property
            def link(self):
                full_link = self.find_element(*self._link_locator).get_attribute('href')
                return full_link.split('?')[0]

            @property
            def name(self):
                return self.find_element(*self._name_locator).text

            @property
            def price(self):
                return self.find_element(*self._price_locator).text

            def click(self):
                self.find_element(*self._name_locator).click()
                from pages.mobile.details import Details
                return Details(self.testsetup)


class Header(Page):

    _search_toggle_locator = (By.CSS_SELECTOR, '.header--search-toggle')
    _search_input_locator = (By.ID, 'search-q')
    _back_button_locator = (By.CSS_SELECTOR, '.header-button.back')
    _marketplace_icon_locator = (By.CSS_SELECTOR, '.wordmark')

    def search(self, search_term):
        """
        Searches for an app using the available search field
        :Args:
         - search_term - string value of the search field
        """
        self.selenium.find_element(*self._search_toggle_locator).click()
        search_field = self.selenium.find_element(*self._search_input_locator)
        WebDriverWait(self.selenium, self.timeout).until(lambda s: search_field.is_displayed())
        search_field.send_keys(search_term)
        search_field.submit()
        from pages.mobile.search import Search
        return Search(self.testsetup)

    def search_and_click_on_app(self, search_term):

        search_page = self.search(search_term)

        # Select the application link in the list
        # It can't always be the first in the list
        results = search_page.results()
        for i in range(len(results)):
            if search_term == results[i].name:
                return results[i].click()

    def click_back(self):
        self.selenium.find_element(*self._back_button_locator).click()

    def click_marketplace_icon(self):
        self.selenium.find_element(*self._marketplace_icon_locator).click()
        from pages.mobile.home import Home
        return Home(self.testsetup)

    @property
    def is_back_button_visible(self):
        return self.is_element_visible(*self._back_button_locator)


class NavMenu(Base):

    _nav_menu_toggle_locator = (By.CSS_SELECTOR, 'mkt-nav-toggle button')
    _nav_menu_locator = (By.TAG_NAME, 'mkt-nav-root')
    _settings_menu_item_locator = (By.CSS_SELECTOR, '.mkt-nav--link[href*="settings"]')
    _sign_in_menu_item_locator = (By.CSS_SELECTOR, '.mkt-nav--link.persona:not(.register)')
    _new_menu_item_locator = (By.CSS_SELECTOR, '.mkt-nav--link[href*="new"]')
    _popular_menu_item_locator = (By.CSS_SELECTOR, '.mkt-nav--link[href*="popular"]')
    _categories_menu_item_locator = (By.CSS_SELECTOR, '.mkt-nav--link[title="Categories"]')

    def open(self):
        menu = self.selenium.find_element(*self._nav_menu_locator)
        if not menu.is_displayed():
            self.selenium.find_element(*self._nav_menu_toggle_locator).click()
            WebDriverWait(self.selenium, self.timeout).until(lambda s: menu.is_displayed())

    def click_settings(self):
        self.open()
        settings_item = self.selenium.find_element(*self._settings_menu_item_locator)
        self.scroll_to_element(settings_item)
        settings_item.click()
        from pages.mobile.settings import Settings
        return Settings(self.testsetup)

    def click_sign_in(self):
        self.open()
        sign_in_item = self.selenium.find_element(*self._sign_in_menu_item_locator)
        self.scroll_to_element(sign_in_item)
        sign_in_item.click()

    def click_new(self):
        self.open()
        new_item = self.selenium.find_element(*self._new_menu_item_locator)
        self.scroll_to_element(new_item)
        new_item.click()
        return self.new_apps

    def click_popular(self):
        self.open()
        popular_item = self.selenium.find_element(*self._popular_menu_item_locator)
        self.scroll_to_element(popular_item)
        popular_item.click()
        return self.popular_apps

    def click_categories(self):
        self.open()
        categories_item = self.selenium.find_element(*self._categories_menu_item_locator)
        self.scroll_to_element(categories_item)
        categories_item.click()
        return self.Categories(self.testsetup)

    class Categories(Page):

        _category_item_locator = (By.CSS_SELECTOR, '#categories mkt-category-item')

        def __init__(self, testsetup):
            Page.__init__(self, testsetup)
            # Wait for the first category to be visible
            element = self.selenium.find_element(*self._category_item_locator)
            WebDriverWait(self.selenium, self.timeout).until(lambda s: element.is_displayed())

        @property
        def categories(self):
            return [self.CategoryItem(self.testsetup, web_element)
                    for web_element in self.selenium.find_elements(*self._category_item_locator)]

        class CategoryItem(PageRegion):

            _category_link_locator = (By.CSS_SELECTOR, '.mkt-category-link')

            @property
            def name(self):
                return self.find_element(*self._category_link_locator).text

            @property
            def link_to_category_page(self):
                return self.find_element(*self._category_link_locator).get_attribute("href")

            def click_category(self):
                category_name = self.name
                self.find_element(*self._category_link_locator).click()
                from pages.desktop.consumer_pages.category import Category
                return Category(self.testsetup, category_name)
