"""Base class for page objects: explicit waits and platform-aware locators."""

import logging

from appium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import Settings, get_settings
from core.locator import Locator, LocatorTuple

LOGGER = logging.getLogger(__name__)


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

    def find_all(self, locator: Locator, timeout: float | None = None) -> list[WebElement]:
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