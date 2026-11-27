"""Checkout screen"""

from appium.webdriver.common.appiumby import AppiumBy

from core.locator import Locator
from pages.base_page import BasePage

APP_ID = "com.saucelabs.mydemoapp.android:id"


def _by_id(name: str, description: str) -> Locator:
    # TODO(ios): the iOS values are temporary, I need an iOS UI dump to get the real ones.
    return Locator(
        android=(AppiumBy.ID, f"{APP_ID}/{name}"),
        ios=(AppiumBy.ACCESSIBILITY_ID, f"TODO-ios-{name}"),
        description=description,
    )


FULL_NAME = _by_id("fullNameET", "Full name field")
ADDRESS_LINE_1 = _by_id("address1ET", "Address line 1 field")
ADDRESS_LINE_2 = _by_id("address2ET", "Address line 2 field")
CITY = _by_id("cityET", "City field")
ZIP_CODE = _by_id("zipET", "Zip code field")
STATE = _by_id("stateET", "State field")
COUNTRY = _by_id("countryET", "Country field")
TO_PAYMENT = Locator.shared(
    AppiumBy.ACCESSIBILITY_ID, "Saves user info for checkout", "To Payment button"
)


class CheckoutPage(BasePage):
    """Shipping address step of the checkout."""

    def is_loaded(self) -> bool:
        # the title is shared with the review screen, so we wait for a field
        return self.is_displayed(FULL_NAME, timeout=10)

    def fill_address(
        self,
        *,
        full_name: str,
        address_line_1: str,
        city: str,
        zip_code: str,
        country: str,
        address_line_2: str = "",
        state: str = "",
    ) -> None:
        fields = [
            (FULL_NAME, full_name),
            (ADDRESS_LINE_1, address_line_1),
            (ADDRESS_LINE_2, address_line_2),
            (CITY, city),
            (ZIP_CODE, zip_code),
            (STATE, state),
            (COUNTRY, country),
        ]
        for locator, value in fields:
            # optional fields are skipped when empty
            if value:
                self.fill(locator, value)

    def go_to_payment(self) -> None:
        self.hide_keyboard()
        self.click(TO_PAYMENT)
