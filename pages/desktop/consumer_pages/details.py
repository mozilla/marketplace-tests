#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from pages.desktop.consumer_pages.base import Base
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.page import Page


class Details(Base):
    """APP details page
    https://marketplace-dev.allizom.org/en-US/app/ app name
    app_name => the name of the app displayed
    """

    _purchase_locator = (By.CSS_SELECTOR, "section.product-details > div.actions > a.premium")
    _install_purchased_locator = (By.CSS_SELECTOR, "section.product-details > div.actions > a.premium.purchased.installing")
    _install_locator = (By.CSS_SELECTOR, "section.product-details > div.actions > a.install")
    _submit_review_link_locator = (By.ID, 'add-first-review')
    _statistics_link_locator = (By.CSS_SELECTOR, "p.view-stats a.arrow")
    _image_locator = (By.CSS_SELECTOR, ".product-details > .visual > img")
    _name_locator = (By.CSS_SELECTOR, ".product-details .vitals.c > h1.oneline")
    _app_dev_username_locator = (By.CSS_SELECTOR, ".vitals.c > .authors.oneline.wide > a")
    _weekly_downloads_locator = (By.CSS_SELECTOR, ".product-details > .vitals > .downloads")
    _section_device_icon_locator = (By.CSS_SELECTOR, ".vitals.c > .device-list.c > ul")
    _application_description_locator = (By.CSS_SELECTOR, ".description > .summary")
    _image_preview_section_locator = (By.CSS_SELECTOR, ".previews.slider.full > .alt-slider")
    _support_email_locator = (By.CSS_SELECTOR, ".contact-support > .support-email > .arrow")
    _privacy_policy_locator = (By.CSS_SELECTOR, ".wide > .more-info > .privacy > .arrow")
    _published_date_locator = (By.CSS_SELECTOR, ".wide > .published > p > time")
    _app_expanded_description_locator = (By.CSS_SELECTOR, "div.more")
    _expand_description_locator = (By.CSS_SELECTOR, "a.collapse.wide")
    _collapse_description_locator = (By.CSS_SELECTOR, "a.collapse.wide.expanded.show")

    def __init__(self, testsetup, app_name=False):
        Base.__init__(self, testsetup)
        self.wait_for_ajax_on_page_finish()
        if app_name:
            self._page_title = "%s | Mozilla Marketplace" % app_name
            self.app_name = app_name

    @property
    def is_app_available_for_purchase(self):
        return self.is_element_visible(*self._purchase_locator)

    @property
    def is_app_installing(self):
        return self.is_element_visible(*self._install_purchased_locator)

    @property
    def is_submit_review_link_visible(self):
        return self.is_element_visible(*self._submit_review_link_locator)

    @property
    def submit_review_link(self):
        return self.selenium.find_element(*self._submit_review_link_locator).text

    @property
    def name(self):
        return self.selenium.find_element(*self._name_locator).text

    @property
    def app_dev_username(self):
        return self.is_element_visible(*self._app_dev_username_locator)

    @property
    def are_weekly_downloads_visible(self):
        return self.is_element_visible(*self._weekly_downloads_locator)

    @property
    def is_image_visible(self):
        return self.is_element_visible(*self._image_locator)

    @property
    def are_section_devices_visible(self):
        return self.is_element_visible(*self._section_device_icon_locator)

    @property
    def is_application_description_visible(self):
        return self.is_element_visible(*self._application_description_locator)

    @property
    def is_image_preview_section_visible(self):
        return self.is_element_visible(*self._image_preview_section_locator)

    @property
    def previewer(self):
        return self.ImagePreviewer(self.testsetup)

    class ImagePreviewer(Page):

        _screenshot_locator = (By.CSS_SELECTOR, '.content li')
        _link_locator = (By.TAG_NAME, 'a')

        def click_image(self, image_no=0):
            images = self.selenium.find_elements(*self._screenshot_locator)
            images[image_no].find_element(*self._link_locator).click()
            from pages.desktop.regions.lightbox import Lightbox
            image_viewer = Lightbox(self.testsetup)
            WebDriverWait(self.selenium, 10).until(lambda s: image_viewer.is_visible)
            return image_viewer

        def image_title(self, image_no):
            return self.selenium.find_element(self._screenshot_locator[0],
                        '%s:nth-child(%s) a' % (self._screenshot_locator[1], image_no + 1)).get_attribute('title')

        def image_link(self, image_no):
            return self.selenium.find_element(self._screenshot_locator[0],
                        '%s:nth-child(%s) a' % (self._screenshot_locator[1], image_no + 1)).get_attribute('href')

        @property
        def image_count(self):
            return len(self.selenium.find_elements(*self._screenshot_locator))

        @property
        def image_set_count(self):
            if self.image_count % 3 == 0:
                return self.image_count / 3
            else:
                return self.image_count / 3 + 1

    @property
    def is_support_email_visible(self):
        return self.is_element_visible(*self._support_email_locator)

    @property
    def is_privacy_policy_link_visible(self):
        return self.is_element_visible(*self._privacy_policy_locator)

    @property
    def is_published_date_visible(self):
        return self.is_element_visible(*self._published_date_locator)

    @property
    def is_install_button_visible(self):
        return self.is_element_visible(*self._install_locator)

    @property
    def install_purchased_button_visible(self):
        return self.is_element_visible(*self._install_purchased_locator)

    @property
    def purchased_button_visible(self):
        return self.is_element_visible(*self._purchase_locator)

    def click_purchase(self):
        self.selenium.find_element(*self._purchase_locator).click()
        return self.PreApproval(self.testsetup)

    def click_statistics(self):
        self.selenium.find_element(*self._statistics_link_locator).click()
        from pages.desktop.consumer_pages.statistics import Statistics
        return Statistics(self.testsetup)

    def click_submit_review(self):
        self.selenium.find_element(*self._submit_review_link_locator).click()
        from pages.desktop.consumer_pages.add_review import AddReview
        return AddReview(self.testsetup, self.app_name)

    @property
    def app_summary_text(self):
        return self.selenium.find_element(*self._application_description_locator).text

    @property
    def app_expanded_description_text(self):
        return self.selenium.find_element(*self._app_expanded_description_locator).text

    @property
    def is_app_description_expanded(self):
        return self.is_element_visible(*self._collapse_description_locator)

    def expand_app_description(self):
        self.selenium.find_element(*self._expand_description_locator).click()

    def collapse_app_description(self):
        self.selenium.find_element(*self._collapse_description_locator).click()

    @property
    def is_app_expanded_description_visible(self):
        return self.is_element_visible(*self._app_expanded_description_locator)

    class PreApproval(Page):
        _root_locator = (By.ID, 'pay')
        _one_time_payment_locator = (By.ID, 'payment-confirm')

        def __init__(self, testsetup):
            Page.__init__(self, testsetup)
            self._root_element = self.selenium.find_element(*self._root_locator)

        @property
        def is_visible(self):
            return self._root_element.is_displayed()

        def click_one_time_payment(self):
            self.selenium.find_element(*self._one_time_payment_locator).click()
            from pages.desktop.paypal.paypal_frame import PayPalFrame
            return PayPalFrame(self.testsetup)
