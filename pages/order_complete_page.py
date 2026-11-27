"""Order confirmation screen."""

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


TITLE = _by_id("completeTV", "Checkout complete title")
THANK_YOU = _by_id("thankYouTV", "Thank you message")
CONTINUE_SHOPPING = Locator.shared(
    AppiumBy.ACCESSIBILITY_ID, "Tap to open catalog", "Continue Shopping button"
)


class OrderCompletePage(BasePage):
    """Confirmation shown after the order is placed."""

    def is_loaded(self) -> bool:
        return self.is_displayed(TITLE, timeout=10)

    def title(self) -> str:
        return self.text_of(TITLE)

    def thank_you_message(self) -> str:
        return self.text_of(THANK_YOU)

    def continue_shopping(self) -> None:
        self.click(CONTINUE_SHOPPING)
