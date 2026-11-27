"""Base class for page objects: explicit waits and platform-aware locators."""

import logging

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import Settings, get_settings
from core.gestures import scroll_down
from core.locator import Locator, LocatorTuple

LOGGER = logging.getLogger(__name__)

APP_ID = "com.saucelabs.mydemoapp.android:id"

# the header is on every screen, so these locators live in the base page
CART_BUTTON = Locator.shared(AppiumBy.ACCESSIBILITY_ID, "View cart", "Cart button")
MENU_BUTTON = Locator.shared(AppiumBy.ACCESSIBILITY_ID, "View menu", "Menu button")
# TODO(ios): the iOS value is temporary, I need an iOS UI dump to get the real one.
CART_BADGE = Locator(
    android=(AppiumBy.ID, f"{APP_ID}/cartTV"),
    ios=(AppiumBy.ACCESSIBILITY_ID, "TODO-ios-cart-badge"),
    description="Cart badge",
)


class BasePage:
    """Shared behaviour for every page. Pages declare locators, tests call actions."""

    def __init__(
        self, driver: webdriver.Remote, settings: Settings | None = None
    ) -> None:
        cfg = settings or get_settings()
        self.driver = driver
        self._platform = cfg.platform
        self._timeout = cfg.explicit_wait_timeout

    # --- Internals -------------------------------------------------------
    def _resolve(self, locator: Locator) -> LocatorTuple:
        return locator.for_platform(self._platform)

    def _wait(self, timeout: float | None = None) -> WebDriverWait:
        return WebDriverWait(self.driver, timeout or self._timeout)

    @staticmethod
    def _label(locator: Locator, resolved: LocatorTuple) -> str:
        return f"{locator.description or resolved[1]} ({resolved[0]}={resolved[1]})"

    # --- Finding elements ------------------------------------------------
    def find(self, locator: Locator, timeout: float | None = None) -> WebElement:
        """Wait until the element is visible and return it."""
        resolved = self._resolve(locator)
        try:
            return self._wait(timeout).until(ec.visibility_of_element_located(resolved))
        except TimeoutException as exc:
            raise TimeoutException(
                f"Element not visible: {self._label(locator, resolved)}"
            ) from exc

    def find_all(
        self, locator: Locator, timeout: float | None = None
    ) -> list[WebElement]:
        """Wait until at least one match is present and return all matches."""
        resolved = self._resolve(locator)
        try:
            return self._wait(timeout).until(
                ec.presence_of_all_elements_located(resolved)
            )
        except TimeoutException as exc:
            raise TimeoutException(
                f"No element found: {self._label(locator, resolved)}"
            ) from exc

    def is_displayed(self, locator: Locator, timeout: float = 3) -> bool:
        """Return True if the element becomes visible within a short delay."""
        try:
            self.find(locator, timeout)
        except TimeoutException:
            return False
        return True

    def scroll_to(self, locator: Locator, max_swipes: int = 8) -> None:
        """Scroll down until the element is visible, or fail with a clear message."""
        for _ in range(max_swipes):
            if self.is_displayed(locator, timeout=1):
                return
            scroll_down(self.driver)
        if not self.is_displayed(locator, timeout=1):
            resolved = self._resolve(locator)
            raise TimeoutException(
                f"Not found after {max_swipes} swipes: {self._label(locator, resolved)}"
            )

    # --- Actions ---------------------------------------------------------
    def click(self, locator: Locator, timeout: float | None = None) -> None:
        resolved = self._resolve(locator)
        try:
            element = self._wait(timeout).until(ec.element_to_be_clickable(resolved))
        except TimeoutException as exc:
            raise TimeoutException(
                f"Element not clickable: {self._label(locator, resolved)}"
            ) from exc
        LOGGER.info("Click: %s", self._label(locator, resolved))
        element.click()

    def type_text(self, locator: Locator, text: str) -> None:
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def text_of(self, locator: Locator) -> str:
        return self.find(locator).text

    def fill(self, locator: Locator, text: str) -> None:
        """Scroll to the field if needed, then type the text."""
        self.scroll_to(locator)
        self.type_text(locator, text)
        self.hide_keyboard()

    def hide_keyboard(self) -> None:
        # the keyboard can cover the buttons at the bottom of the screen
        try:
            self.driver.hide_keyboard()
        except WebDriverException:
            pass  # no keyboard on screen

    # --- Header (visible on every screen) --------------------------------
    def open_cart(self) -> None:
        self.click(CART_BUTTON)

    def open_menu(self) -> None:
        self.click(MENU_BUTTON)

    def cart_count(self) -> int:
        """Number shown on the cart badge (0 when there is no badge)."""
        # the badge only exists when the cart has items
        if not self.is_displayed(CART_BADGE, timeout=5):
            return 0
        return int(self.text_of(CART_BADGE))
