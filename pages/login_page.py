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
USERNAME_ERROR = Locator(
    android=(AppiumBy.ID, f"{APP_ID}/nameErrorTV"),
    ios=(AppiumBy.ACCESSIBILITY_ID, "TODO-ios-username-error"),
    description="Username error",
)
PASSWORD_ERROR = Locator(
    android=(AppiumBy.ID, f"{APP_ID}/passwordErrorTV"),
    ios=(AppiumBy.ACCESSIBILITY_ID, "TODO-ios-password-error"),
    description="Password error",
)
LOGIN_BUTTON = Locator.shared(
    AppiumBy.ACCESSIBILITY_ID, "Tap to login with given credentials", "Login button"
)


def saved_user(name: str) -> Locator:
    """Entry of the saved users list, found by its text."""
    xpath = (
        '//android.widget.TextView[@content-desc="Tap to use this username for login"'
        f' and @text="{name}"]'
    )
    return Locator(
        android=(AppiumBy.XPATH, xpath),
        ios=(AppiumBy.ACCESSIBILITY_ID, "TODO-ios-saved-user"),
        description=f"Saved user {name}",
    )


class LoginPage(BasePage):
    """Login form with username and password."""

    def is_loaded(self) -> bool:
        return self.is_displayed(TITLE, timeout=10)

    def login(self, username: str, password: str) -> None:
        # empty values are skipped, so we can also test the empty form
        if username:
            self.type_text(USERNAME, username)
        if password:
            self.type_text(PASSWORD, password)
        self.submit()

    def select_saved_user(self, name: str) -> None:
        """Tap a user in the list, the app fills both fields."""
        self.click(saved_user(name))

    def submit(self) -> None:
        self._hide_keyboard()
        self.click(LOGIN_BUTTON)

    def error_message(self, field: str) -> str:
        """Error text shown under the 'username' or the 'password' field."""
        locator = USERNAME_ERROR if field == "username" else PASSWORD_ERROR
        return self.text_of(locator)

    def _hide_keyboard(self) -> None:
        # the keyboard can cover the login button
        try:
            self.driver.hide_keyboard()
        except WebDriverException:
            pass  # no keyboard on screen
