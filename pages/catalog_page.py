"""Catalog screen: product list, sorting, cart and menu entry points."""

from appium.webdriver.common.appiumby import AppiumBy

from core.gestures import scroll_down
from core.locator import Locator
from pages.base_page import BasePage

APP_ID = "com.saucelabs.mydemoapp.android:id"

# TODO(ios): the iOS values are temporary, I need an iOS UI dump to get the real ones.
TITLE = Locator(
    android=(AppiumBy.ID, f"{APP_ID}/productTV"),
    ios=(AppiumBy.ACCESSIBILITY_ID, "TODO-ios-catalog-title"),
    description="Catalog title",
)
PRODUCT_TITLES = Locator(
    android=(AppiumBy.ID, f"{APP_ID}/titleTV"),
    ios=(AppiumBy.ACCESSIBILITY_ID, "Product Title"),
    description="Product titles",
)
CART_BUTTON = Locator.shared(AppiumBy.ACCESSIBILITY_ID, "View cart", "Cart button")
MENU_BUTTON = Locator.shared(AppiumBy.ACCESSIBILITY_ID, "View menu", "Menu button")


def product_image(name: str) -> Locator:
    """Image of the product that has this exact title (same card as the title)."""
    xpath = (
        f'//android.widget.TextView[@resource-id="{APP_ID}/titleTV" and @text="{name}"]'
        '/parent::*//android.widget.ImageView[@content-desc="Product Image"]'
    )
    return Locator(
        android=(AppiumBy.XPATH, xpath),
        ios=(AppiumBy.ACCESSIBILITY_ID, "TODO-ios-product-image"),
        description=f"Image of {name}",
    )


class CatalogPage(BasePage):
    """The product catalog shown when the app starts."""

    def is_loaded(self) -> bool:
        return self.is_displayed(TITLE, timeout=10)

    def visible_product_titles(self) -> list[str]:
        return [element.text for element in self.find_all(PRODUCT_TITLES)]

    def open_product(self, name: str, max_swipes: int = 8) -> None:
        """Scroll the list until the product is visible, then open it."""
        for _ in range(max_swipes):
            # the list only loads the products that are on screen
            if name in self.visible_product_titles():
                # the title is not clickable, so we tap the product image
                self.click(product_image(name))
                return
            scroll_down(self.driver)
        raise LookupError(f"Product not found after {max_swipes} swipes: {name!r}")

    def open_cart(self) -> None:
        self.click(CART_BUTTON)

    def open_menu(self) -> None:
        self.click(MENU_BUTTON)