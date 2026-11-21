"""W3C Actions gestures (no TouchAction): cross-platform scroll and swipe."""

from typing import Literal

from appium import webdriver
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.remote.webelement import WebElement

type Direction = Literal["left", "right"]


def swipe(
    driver: webdriver.Remote,
    start_x: int,
    start_y: int,
    end_x: int,
    end_y: int,
    duration_ms: int = 600,
) -> None:
    """Drag one finger from a start point to an end point."""
    finger = PointerInput(interaction.POINTER_TOUCH, "finger")
    actions = ActionBuilder(driver, mouse=finger, duration=duration_ms)
    actions.pointer_action.move_to_location(start_x, start_y)
    actions.pointer_action.pointer_down()
    actions.pointer_action.move_to_location(end_x, end_y)
    actions.pointer_action.release()
    actions.perform()


def scroll_down(driver: webdriver.Remote) -> None:
    """Move the content up (finger swipes upward) to reveal what is below."""
    size = driver.get_window_size()
    x = size["width"] // 2
    swipe(driver, x, int(size["height"] * 0.75), x, int(size["height"] * 0.35))


def scroll_up(driver: webdriver.Remote) -> None:
    """Move the content down (finger swipes downward) to reveal what is above."""
    size = driver.get_window_size()
    x = size["width"] // 2
    swipe(driver, x, int(size["height"] * 0.35), x, int(size["height"] * 0.75))


def swipe_element(
    driver: webdriver.Remote,
    element: WebElement,
    direction: Direction = "left",
    distance_ratio: float = 0.8,
) -> None:
    """Swipe horizontally across an element (e.g. to delete a cart item)."""
    rect = element.rect
    y = rect["y"] + rect["height"] // 2
    left = rect["x"] + int(rect["width"] * (1 - distance_ratio))
    right = rect["x"] + int(rect["width"] * distance_ratio)
    if direction == "left":
        swipe(driver, right, y, left, y)
    else:
        swipe(driver, left, y, right, y)
