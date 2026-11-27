"""Side menu."""

from appium.webdriver.common.appiumby import AppiumBy

from core.locator import Locator
from pages.base_page import BasePage

APP_ID = "com.saucelabs.mydemoapp.android:id"

# TODO(ios): the iOS value is temporary, I need an iOS UI dump to get the real one.
MENU_LIST = Locator(
    android=(AppiumBy.ACCESSIBILITY_ID, "Recycler view for menu"),
    ios=(AppiumBy.ACCESSIBILITY_ID, "TODO-ios-menu-list"),
    description="Menu list",
)


def menu_item(name: str) -> Locator:
    """Menu entry found by its text (every entry shares the same id)."""
    xpath = (
        f'//android.widget.TextView[@resource-id="{APP_ID}/itemTV" and @text="{name}"]'
    )
    return Locator(
        android=(AppiumBy.XPATH, xpath),
        ios=(AppiumBy.ACCESSIBILITY_ID, "TODO-ios-menu-item"),
        description=f"Menu item {name}",
    )


class MenuPage(BasePage):
    """The drawer menu opened from the header."""

    def go_to(self, name: str) -> None:
        self.open_menu()
        assert self.is_displayed(MENU_LIST, timeout=5)
        self.click(menu_item(name))
