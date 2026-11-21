"""Product detail screen."""

from appium.webdriver.common.appiumby import AppiumBy

from core.locator import Locator
from pages.base_page import BasePage

APP_ID = "com.saucelabs.mydemoapp.android:id"

# TODO(ios): the iOS values are temporary, I need an iOS UI dump to get the real ones.
TITLE = Locator(
    android=(AppiumBy.ID, f"{APP_ID}/productTV"),
    ios=(AppiumBy.ACCESSIBILITY_ID, "TODO-ios-product-title"),
    description="Product title",
)
PRICE = Locator(
    android=(AppiumBy.ID, f"{APP_ID}/priceTV"),
    ios=(AppiumBy.ACCESSIBILITY_ID, "TODO-ios-product-price"),
    description="Product price",
)
QUANTITY = Locator(
    android=(AppiumBy.ID, f"{APP_ID}/noTV"),
    ios=(AppiumBy.ACCESSIBILITY_ID, "TODO-ios-quantity"),
    description="Selected quantity",
)
PRODUCT_IMAGE = Locator(
    android=(AppiumBy.ACCESSIBILITY_ID, "Displays selected product"),
    ios=(AppiumBy.ACCESSIBILITY_ID, "TODO-ios-product-image"),
    description="Product image",
)
INCREASE = Locator.shared(
    AppiumBy.ACCESSIBILITY_ID, "Increase item quantity", "Increase quantity"
)
ADD_TO_CART = Locator.shared(
    AppiumBy.ACCESSIBILITY_ID, "Tap to add product to cart", "Add to cart button"
)


def color(name: str) -> Locator:
    """Locator for a color swatch, e.g. color("Blue")."""
    return Locator.shared(AppiumBy.ACCESSIBILITY_ID, f"{name} color", f"{name} color")


class ProductPage(BasePage):
    """Detail page of one product."""

    def is_loaded(self) -> bool:
        """Check that the product page is open."""
        # the title id is also used on the catalog, so we wait for the product image
        return self.is_displayed(PRODUCT_IMAGE, timeout=10)

    def title(self) -> str:
        # the title is at the top, so read it before any scroll
        return self.text_of(TITLE)

    def price(self) -> str:
        # the price is below the fold
        self.scroll_to(PRICE)
        return self.text_of(PRICE)

    def quantity(self) -> int:
        self.scroll_to(QUANTITY)
        return int(self.text_of(QUANTITY))

    def select_color(self, name: str) -> None:
        self.scroll_to(color(name))
        self.click(color(name))

    def increase_quantity(self) -> None:
        self.scroll_to(INCREASE)
        self.click(INCREASE)

    def add_to_cart(self) -> None:
        """The button is below the fold, so scroll to it first."""
        self.scroll_to(ADD_TO_CART)
        self.click(ADD_TO_CART)