# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import expected
from pages.page import Page, PageRegion


class Base(Page):

    _body_class_locator = (By.CSS_SELECTOR, '#container > #page')
    _notification_locator = (By.ID, 'notification')
    _notification_content_locator = (By.ID, 'notification-content')
    _new_popular_apps_list_locator = (By.CSS_SELECTOR, '.app-list li')
    _feed_title_locator = (By.CSS_SELECTOR, '.subheader > h1')
    _apps_locator = (By.CSS_SELECTOR, '#navigation a[data-nav-type="apps"]')
    _sites_locator = (By.CSS_SELECTOR, '#navigation a[data-nav-type="websites"]')
    _close_banner_button_locator = (By.CLASS_NAME, 'mkt-banner-close')
    _bag_icon_locator = (By.CLASS_NAME, 'mkt-wordmark')
    _sign_in_locator = (By.CSS_SELECTOR, '.account-settings-save a:not(.register)')

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

    def click_apps(self):
        self.selenium.find_element(*self._apps_locator).click()
        from pages.mobile.item_list import ItemList
        return ItemList(self.base_url, self.selenium)

    def click_sites(self):
        self.selenium.find_element(*self._sites_locator).click()
        from pages.mobile.item_list import ItemList
        return ItemList(self.base_url, self.selenium)

    def close_banner(self):
        close_banner_button = self.selenium.find_element(*self._close_banner_button_locator)
        bag_icon = self.selenium.find_element(*self._bag_icon_locator)
        if close_banner_button.is_displayed():
            close_banner_button.click()
            WebDriverWait(self.selenium, self.timeout).until(expected.element_not_moving(bag_icon))

    def wait_notification_box_visible(self):
        self.wait_for_element_visible(*self._notification_locator)

    def wait_notification_box_not_visible(self):
        self.wait_for_element_not_visible(*self._notification_locator)

    def login(self, email, password):
        from fxapom.pages.sign_in import SignIn
        fxa_login = SignIn(self.base_url, self.selenium)
        fxa_login.sign_in(email, password)
        self.wait_notification_box_visible()
        self.wait_notification_box_not_visible()

    @property
    def header(self):
        return Header(self.base_url, self.selenium)

    @property
    def more_menu(self):
        return MoreMenu(self.base_url, self.selenium)

    @property
    def popular_apps(self):
        return [self.Application(self.base_url, self.selenium, web_element)
                for web_element in self.selenium.find_elements(*self._new_popular_apps_list_locator)]

    @property
    def new_apps(self):
        return [self.Application(self.base_url, self.selenium, web_element)
                for web_element in self.selenium.find_elements(*self._new_popular_apps_list_locator)]

    def go_to_first_free_app_page(self):
        results_page = self.header.search(':free')
        return results_page.items()[0].click()

    @property
    def is_sign_in_visible(self):
        return self.is_element_visible(*self._sign_in_locator)

    class Application(PageRegion):

            _name_locator = (By.CSS_SELECTOR, '.mkt-product-name')

            @property
            def name(self):
                return self.find_element(*self._name_locator).text


class Header(Page):

    _search_toggle_locator = (By.CLASS_NAME, 'mkt-search-btn')
    _search_input_locator = (By.ID, 'search-q')
    _back_button_locator = (By.CLASS_NAME, 'header-back-btn')
    _marketplace_icon_locator = (By.CLASS_NAME, 'mkt-wordmark')

    def search(self, search_term):
        """
        Searches for an app using the available search field
        :Args:
         - search_term - string value of the search field
        """
        self.selenium.find_element(*self._search_toggle_locator).click()
        search_field = self.selenium.find_element(*self._search_input_locator)
        WebDriverWait(self.selenium, self.timeout).until(expected.element_not_moving(search_field))
        search_field.send_keys(search_term)
        search_field.submit()
        from pages.mobile.search import Search
        return Search(self.base_url, self.selenium)

    def search_and_click_on_app(self, search_term):

        search_page = self.search(search_term)

        # Select the application link in the list
        # It can't always be the first in the list
        results = search_page.items()
        for i in range(len(results)):
            if search_term == results[i].name:
                return results[i].click()

    def click_back(self):
        self.selenium.find_element(*self._back_button_locator).click()

    def click_marketplace_icon(self):
        self.selenium.find_element(*self._marketplace_icon_locator).click()
        from pages.mobile.home import Home
        return Home(self.base_url, self.selenium)

    @property
    def is_back_button_visible(self):
        return self.is_element_visible(*self._back_button_locator)


class MoreMenu(Base):

    _more_menu_toggle_locator = (By.CSS_SELECTOR, '#navigation a[data-nav-type="more"]')
    _more_menu_locator = (By.CLASS_NAME, 'more-menu-overlay')
    _settings_menu_item_locator = (By.CLASS_NAME, 'more-menu-settings')
    _sign_in_menu_item_locator = (By.CLASS_NAME, 'more-menu-sign-in')
    _sign_out_menu_item_locator = (By.CLASS_NAME, 'more-menu-sign-out')
    _new_menu_item_locator = (By.CSS_SELECTOR, '.mkt-nav--link[href*="new"]')
    _popular_menu_item_locator = (By.CSS_SELECTOR, '.mkt-nav--link[href*="popular"]')
    _categories_menu_item_locator = (By.CSS_SELECTOR, '.mkt-nav--link[title="Categories"]')

    def open(self):
        menu = self.selenium.find_element(*self._more_menu_locator)
        if 'overlay-visible' not in menu.get_attribute('class'):
            self.selenium.find_element(*self._more_menu_toggle_locator).click()
            WebDriverWait(self.selenium, self.timeout).until(expected.element_not_moving(menu))

    def click_settings(self):
        self.open()
        settings_item = self.selenium.find_element(*self._settings_menu_item_locator)
        self.scroll_to_element(settings_item)
        settings_item.click()
        from pages.mobile.settings import Settings
        return Settings(self.base_url, self.selenium)

    def click_sign_in(self):
        self.open()
        sign_in_item = self.selenium.find_element(*self._sign_in_menu_item_locator)
        self.scroll_to_element(sign_in_item)
        sign_in_item.click()

    def click_sign_out(self):
        self.open()
        el = self.selenium.find_element(*self._sign_out_menu_item_locator)
        self.scroll_to_element(el)
        el.click()
        from pages.mobile.home import Home
        home = Home(self.base_url, self.selenium)
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: home.is_sign_in_visible)
        return home
