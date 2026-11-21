"""Cart screen."""

from appium.webdriver.common.appiumby import AppiumBy

from core.locator import Locator
from pages.base_page import BasePage

APP_ID = "com.saucelabs.mydemoapp.android:id"

# TODO(ios): the iOS values are temporary, I need an iOS UI dump to get the real ones.
CART_LIST = Locator(
    android=(AppiumBy.ACCESSIBILITY_ID, "Displays list of selected products"),
    ios=(AppiumBy.ACCESSIBILITY_ID, "TODO-ios-cart-list"),
    description="Cart list",
)
ITEM_TITLES = Locator(
    android=(AppiumBy.ID, f"{APP_ID}/titleTV"),
    ios=(AppiumBy.ACCESSIBILITY_ID, "TODO-ios-cart-item-title"),
    description="Cart item titles",
)
TOTAL_PRICE = Locator(
    android=(AppiumBy.ID, f"{APP_ID}/totalPriceTV"),
    ios=(AppiumBy.ACCESSIBILITY_ID, "TODO-ios-total-price"),
    description="Total price",
)
REMOVE_ITEM = Locator.shared(
    AppiumBy.ACCESSIBILITY_ID, "Removes product from cart", "Remove item button"
)
CHECKOUT = Locator.shared(
    AppiumBy.ACCESSIBILITY_ID, "Confirms products for checkout", "Checkout button"
)


class CartPage(BasePage):
    """The cart with its items and the checkout button."""

    def is_loaded(self) -> bool:
        # the title id is shared with other screens, so we wait for the cart list
        return self.is_displayed(CART_LIST, timeout=10)

    def item_titles(self) -> list[str]:
        return [element.text for element in self.find_all(ITEM_TITLES)]

    def total_price(self) -> str:
        return self.text_of(TOTAL_PRICE)

    def remove_item(self) -> None:
        self.click(REMOVE_ITEM)

    def proceed_to_checkout(self) -> None:
        self.click(CHECKOUT)
