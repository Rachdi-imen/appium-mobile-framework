"""Login screen."""

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import WebDriverException

from core.locator import Locator
from pages.base_page import BasePage

APP_ID = "com.saucelabs.mydemoapp.android:id"

# TODO(ios): the iOS values are temporary, I need an iOS UI dump to get the real ones.
TITLE = Locator(
    android=(AppiumBy.ID, f"{APP_ID}/loginTV"),
    ios=(AppiumBy.ACCESSIBILITY_ID, "TODO-ios-login-title"),
    description="Login title",
)
USERNAME = Locator(
    android=(AppiumBy.ID, f"{APP_ID}/nameET"),
    ios=(AppiumBy.ACCESSIBILITY_ID, "TODO-ios-username"),
    description="Username field",
)
PASSWORD = Locator(
    android=(AppiumBy.ID, f"{APP_ID}/passwordET"),
    ios=(AppiumBy.ACCESSIBILITY_ID, "TODO-ios-password"),
    description="Password field",
)
LOGIN_BUTTON = Locator.shared(
    AppiumBy.ACCESSIBILITY_ID, "Tap to login with given credentials", "Login button"
)


class LoginPage(BasePage):
    """Login form with username and password."""

    def is_loaded(self) -> bool:
        return self.is_displayed(TITLE, timeout=10)

    def login(self, username: str, password: str) -> None:
        self.type_text(USERNAME, username)
        self.type_text(PASSWORD, password)
        self._hide_keyboard()
        self.click(LOGIN_BUTTON)

    def _hide_keyboard(self) -> None:
        try:
            self.driver.hide_keyboard()
        except WebDriverException:
            pass  # no keyboard on screen