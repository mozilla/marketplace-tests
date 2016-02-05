# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from time import strptime, mktime

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait

from pages.desktop.developer_hub.base import Base
from pages.desktop.developer_hub.edit_app import EditListing
from pages.page import Page
from pages.page import PageRegion


class DeveloperSubmissions(Base):
    """
    Developer Submissions Page

    https://marketplace-dev.allizom.org/developers/submissions/
    """
    _page_title = "Manage My Submissions | Developers | Firefox Marketplace"

    _app_locator = (By.CSS_SELECTOR, 'div.items > div.item')
    _notification_locator = (By.CSS_SELECTOR, 'div.notification-box')

    def __init__(self, base_url, selenium):
        Base.__init__(self, base_url, selenium)
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: self.selenium.execute_script('return jQuery.active == 0') and
            self.is_the_current_page)

    @property
    def submitted_apps(self):
        return [App(self.base_url, self.selenium, app) for app in self.selenium.find_elements(*self._app_locator)]

    @property
    def first_free_app(self):
        """Return the first free app in the listing."""
        for i in range(1, self.paginator.total_page_number + 1):
            for app in self.submitted_apps:
                if app.has_price and app.price == 'Free' and 'Disabled' not in app.status:
                    return app
            if self.paginator.is_paginator_present:
                if not self.paginator.is_next_page_disabled:
                    self.paginator.click_next_page()
        else:
            raise Exception('App not found')

    @property
    def first_free_hosted_app(self):
        """Return the first free app in the listing."""
        for i in range(1, self.paginator.total_page_number + 1):
            for app in self.submitted_apps:
                if app.has_price and app.price == 'Free' and not app.is_packaged_app:
                    return app
            if self.paginator.is_paginator_present:
                if not self.paginator.is_next_page_disabled:
                    self.paginator.click_next_page()
        else:
            raise Exception('App not found')

    def get_app(self, app_name):
        for i in range(1, self.paginator.total_page_number + 1):
            for app in self.submitted_apps:
                if app_name == app.name:
                    return app
            if self.paginator.is_paginator_present:
                if not self.paginator.is_next_page_disabled:
                    self.paginator.click_next_page()
        else:
            raise Exception('App not found')

    @property
    def is_notification_visible(self):
        return self.is_element_visible(*self._notification_locator)

    @property
    def is_notification_successful(self):
        return 'success' in self.find_element(*self._notification_locator).get_attribute('class')

    @property
    def notification_message(self):
        return self.find_element(*self._notification_locator).text

    @property
    def sorter(self):
        return Sorter(self.base_url, self.selenium)

    @property
    def paginator(self):
        return Paginator(self.base_url, self.selenium)


class App(PageRegion):

    _name_locator = (By.CSS_SELECTOR, 'h3')
    _status_locator = (By.CSS_SELECTOR, '.version-status-item > a > span > b')
    _incomplete_locator = (By.CSS_SELECTOR, 'p.incomplete')
    _created_date_locator = (By.CSS_SELECTOR, 'ul.item-details > li.date-created')
    _price_locator = (By.CSS_SELECTOR, 'ul.item-details > li > span.price')
    _edit_link_locator = (By.CSS_SELECTOR, 'a.action-link')
    _packaged_app_locator = (By.CSS_SELECTOR, '.item-current-version')
    _manage_status_and_version_locator = (By.CSS_SELECTOR, 'a.status-link')
    _compatibility_and_payments_locator = (By.CSS_SELECTOR, 'div.item-actions > ul li a[href$="/payments/"]')
    _date_locator = (By.CLASS_NAME, 'date-created')

    def _is_element_present_in_app(self, *locator):
        self.selenium.implicitly_wait(0)
        try:
            self.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
        finally:
            # set back to where you once belonged
            self.selenium.implicitly_wait(10)

    @property
    def is_incomplete(self):
        return self._is_element_present_in_app(*self._incomplete_locator)

    @property
    def name(self):
        return self.find_element(*self._name_locator).text

    @property
    def status(self):
        return self.find_element(*self._status_locator).text

    @property
    def date(self):
        if not self.is_incomplete:
            date_text = self.find_element(*self._created_date_locator).text
            date = strptime(date_text.split(':')[1], ' %B %d, %Y')
            return mktime(date)

    @property
    def price(self):
        return self.find_element(*self._price_locator).text

    @property
    def is_packaged_app(self):
        return self._is_element_present_in_app(*self._packaged_app_locator)

    @property
    def has_price(self):
        return self._is_element_present_in_app(*self._price_locator)

    @property
    def has_date(self):
        return self._is_element_present_in_app(*self._date_locator)

    def click_edit(self):
        self.find_element(*self._edit_link_locator).click()
        return EditListing(self.base_url, self.selenium)

    def click_manage_status_and_versions(self):
        self.find_element(*self._manage_status_and_version_locator).click()
        from pages.desktop.developer_hub.manage_status import ManageStatus
        return ManageStatus(self.base_url, self.selenium)

    def click_compatibility_and_payments(self):
        self.find_element(*self._compatibility_and_payments_locator).click()
        from pages.desktop.developer_hub.compatibility_and_payments import CompatibilityAndPayments
        return CompatibilityAndPayments(self.base_url, self.selenium)


class Sorter(Page):

    _sorter_base_locator = (By.ID, 'sorter')
    _options_locator = (By.CSS_SELECTOR, 'li > a.opt')
    _selected_locator = (By.CSS_SELECTOR, 'li.selected')

    def __init__(self, base_url, selenium):
        Page.__init__(self, base_url, selenium)
        self._sorter = self.selenium.find_element(*self._sorter_base_locator)

    @property
    def selected(self):
        return self._sorter.find_element(*self._selected_locator).text

    def sort_by(self, value):
        if not value == self.selected:
            for option in self._sorter.find_elements(*self._options_locator):
                if option.text.lower() == value.lower():
                    option.click()


class Paginator(Page):

    _paginator_locator = (By.CSS_SELECTOR, 'nav.paginator')
    _apps_locator = (By.CSS_SELECTOR, 'div.items > div.item')

    # Numbering
    _page_number_locator = (By.CSS_SELECTOR, 'nav.paginator .num > a:nth-child(1)')
    _total_page_number_locator = (By.CSS_SELECTOR, 'nav.paginator .num > a:nth-child(2)')

    # Navigation
    _first_page_locator = (By.CSS_SELECTOR, 'nav.paginator .rel a:nth-child(1)')
    _prev_locator = (By.CSS_SELECTOR, 'nav.paginator .rel a.prev')
    _next_locator = (By.CSS_SELECTOR, 'nav.paginator .rel a.next')
    _last_page_locator = (By.CSS_SELECTOR, 'nav.paginator .rel a:nth-child(4)')

    # Position
    _start_item_number_locator = (By.CSS_SELECTOR, 'nav.paginator .pos b:nth-child(1)')
    _end_item_number_locator = (By.CSS_SELECTOR, 'nav.paginator .pos b:nth-child(2)')
    _total_item_number = (By.CSS_SELECTOR, 'nav.paginator .pos b:nth-child(3)')

    def wait_for_apps_visible(self):
        self.wait_for_element_visible(*self._apps_locator)

    @property
    def is_paginator_present(self):
        return self.is_element_present(*self._paginator_locator)

    @property
    def page_number(self):
        return int(self.selenium.find_element(*self._page_number_locator).text)

    @property
    def total_page_number(self):
        if self.is_paginator_present:
            return int(self.selenium.find_element(*self._total_page_number_locator).text)
        else:
            return 1

    @property
    def is_prev_page_disabled(self):
        return 'disabled' in self.selenium.find_element(*self._prev_locator).get_attribute('class')

    @property
    def is_first_page_disabled(self):
        return 'disabled' in self.selenium.find_element(*self._first_page_locator).get_attribute('class')

    def click_next_page(self):
        self.selenium.find_element(*self._next_locator).click()
        self.wait_for_apps_visible()

    @property
    def is_next_page_disabled(self):
        return 'disabled' in self.selenium.find_element(*self._next_locator).get_attribute('class')

    @property
    def is_last_page_disabled(self):
        return 'disabled' in self.selenium.find_element(*self._last_page_locator).get_attribute('class')

    @property
    def start_item(self):
        return int(self.selenium.find_element(*self._start_item_number_locator).text)

    @property
    def end_item(self):
        return int(self.selenium.find_element(*self._end_item_number_locator).text)

    @property
    def total_items(self):
        return int(self.selenium.find_element(*self._total_item_number).text)
