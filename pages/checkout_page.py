"""Checkout screen (shipping address)."""

from appium.webdriver.common.appiumby import AppiumBy

from core.locator import Locator
from pages.base_page import BasePage

APP_ID = "com.saucelabs.mydemoapp.android:id"

# TODO(ios): the iOS value is temporary, I need an iOS UI dump to get the real one.
TITLE = Locator(
    android=(AppiumBy.ID, f"{APP_ID}/checkoutTitleTV"),
    ios=(AppiumBy.ACCESSIBILITY_ID, "TODO-ios-checkout-title"),
    description="Checkout title",
)


class CheckoutPage(BasePage):
    """Shipping address step of the checkout."""

    def is_loaded(self) -> bool:
        return self.is_displayed(TITLE, timeout=10)
