"""Payment screen."""

import logging

from appium.webdriver.common.appiumby import AppiumBy

from core.locator import Locator
from pages.base_page import BasePage

APP_ID = "com.saucelabs.mydemoapp.android:id"
LOGGER = logging.getLogger(__name__)


def _by_id(name: str, description: str) -> Locator:
    # TODO(ios): the iOS values are temporary, I need an iOS UI dump to get the real ones.
    return Locator(
        android=(AppiumBy.ID, f"{APP_ID}/{name}"),
        ios=(AppiumBy.ACCESSIBILITY_ID, f"TODO-ios-{name}"),
        description=description,
    )


TITLE = _by_id("enterPaymentMethodTV", "Payment title")
CARD_HOLDER = _by_id("nameET", "Card holder field")
CARD_NUMBER = _by_id("cardNumberET", "Card number field")
EXPIRATION = _by_id("expirationDateET", "Expiration date field")
SECURITY_CODE = _by_id("securityCodeET", "Security code field")
BILLING_SAME = Locator.shared(
    AppiumBy.ACCESSIBILITY_ID,
    "Select if User billing address and shipping address are same",
    "Billing address checkbox",
)
REVIEW_ORDER = Locator.shared(
    AppiumBy.ACCESSIBILITY_ID,
    "Saves payment info and launches screen to review checkout data",
    "Review Order button",
)


class PaymentPage(BasePage):
    """Payment step of the checkout."""

    def is_loaded(self) -> bool:
        return self.is_displayed(TITLE, timeout=10)

    def fill_card(
        self, *, holder: str, number: str, expiration: str, security_code: str
    ) -> None:
        self.fill(CARD_HOLDER, holder)
        self.fill(CARD_NUMBER, number)
        self.fill(EXPIRATION, expiration)
        self.fill(SECURITY_CODE, security_code)

    def set_billing_same_as_shipping(self, same: bool) -> None:
        """Make the checkbox match the wanted state, click only if needed."""
        self.scroll_to(BILLING_SAME)
        checkbox = self.find(BILLING_SAME)
        # is_selected() is wrong for this checkbox, so we read 'checked'
        is_checked = checkbox.get_attribute("checked") == "true"
        # a click toggles the box, so we only click when the state is different
        if is_checked != same:
            checkbox.click()

    def review_order(self) -> None:
        self.hide_keyboard()
        # if the billing form is open, the button is below the fold
        self.scroll_to(REVIEW_ORDER)
        self.click(REVIEW_ORDER)
