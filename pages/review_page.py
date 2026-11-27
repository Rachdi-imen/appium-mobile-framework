"""Review order screen."""

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


ORDER_LIST = _by_id("placeOrderRV", "Order items list")
ITEM_TITLES = _by_id("titleTV", "Order item titles")
TOTAL = _by_id("totalAmountTV", "Order total")
PLACE_ORDER = Locator.shared(
    AppiumBy.ACCESSIBILITY_ID, "Completes the process of checkout", "Place Order button"
)


class ReviewPage(BasePage):
    """Last step before the order is placed."""

    def is_loaded(self) -> bool:
        # the list id is only used on this screen
        return self.is_displayed(ORDER_LIST, timeout=10)

    def item_titles(self) -> list[str]:
        return [element.text for element in self.find_all(ITEM_TITLES)]

    def total(self) -> str:
        return self.text_of(TOTAL)

    def place_order(self) -> None:
        self.click(PLACE_ORDER)
