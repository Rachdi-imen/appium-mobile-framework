"""Drawing screen."""

from appium.webdriver.common.appiumby import AppiumBy

from core.gestures import draw_polygon
from core.locator import Locator
from pages.base_page import BasePage

APP_ID = "com.saucelabs.mydemoapp.android:id"

# TODO(ios): the iOS values are temporary, I need an iOS UI dump to get the real ones.
TITLE = Locator(
    android=(AppiumBy.ID, f"{APP_ID}/drawingTV"),
    ios=(AppiumBy.ACCESSIBILITY_ID, "TODO-ios-drawing-title"),
    description="Drawing title",
)
PAD = Locator(
    android=(AppiumBy.ACCESSIBILITY_ID, "Pad to draw on"),
    ios=(AppiumBy.ACCESSIBILITY_ID, "TODO-ios-drawing-pad"),
    description="Drawing pad",
)
SAVE_MESSAGE = Locator(
    android=(AppiumBy.ID, "android:id/message"),
    ios=(AppiumBy.ACCESSIBILITY_ID, "TODO-ios-save-message"),
    description="Save message",
)
CONFIRM_SAVE = Locator(
    android=(AppiumBy.ID, "android:id/button1"),
    ios=(AppiumBy.ACCESSIBILITY_ID, "TODO-ios-save-ok"),
    description="Save dialog OK button",
)
CLEAR = Locator.shared(
    AppiumBy.ACCESSIBILITY_ID, "Removes anything drawn on pad", "Clear button"
)
SAVE = Locator.shared(
    AppiumBy.ACCESSIBILITY_ID, "Save anything drawn on pad", "Save button"
)


class DrawingPage(BasePage):
    """Pad where the user draws, with clear and save buttons."""

    def is_loaded(self) -> bool:
        return self.is_displayed(TITLE, timeout=10)

    def draw_square(self) -> None:
        """Draw a square in the middle of the pad."""
        rect = self.find(PAD).rect
        # the square takes half of the smallest side, so it always fits the pad
        half = min(rect["width"], rect["height"]) // 4
        center_x = rect["x"] + rect["width"] // 2
        center_y = rect["y"] + rect["height"] // 2
        left, right = center_x - half, center_x + half
        top, bottom = center_y - half, center_y + half
        # the first point is repeated at the end to close the shape
        draw_polygon(
            self.driver,
            [(left, top), (right, top), (right, bottom), (left, bottom), (left, top)],
        )

    def clear(self) -> None:
        self.click(CLEAR)

    def save(self) -> None:
        self.click(SAVE)

    def save_message(self) -> str:
        return self.text_of(SAVE_MESSAGE)

    def confirm_save(self) -> None:
        self.click(CONFIRM_SAVE)
