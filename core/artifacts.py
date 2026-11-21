"""Failure diagnostics: screenshots and screen recordings for Allure."""

import base64
import logging

import allure
from appium import webdriver

from config.settings import Settings

LOGGER = logging.getLogger(__name__)


def start_video(driver: webdriver.Remote, settings: Settings) -> bool:
    """Start recording the screen. Returns False if the device cannot record."""
    try:
        driver.start_recording_screen(timeLimit=str(settings.video_time_limit_seconds))
    except Exception:
        LOGGER.warning("Screen recording is unavailable", exc_info=True)
        return False
    LOGGER.info("Screen recording started")
    return True


def stop_video(driver: webdriver.Remote) -> bytes | None:
    """Stop recording and return the video bytes (None if nothing was captured)."""
    try:
        encoded = driver.stop_recording_screen()
    except Exception:
        LOGGER.warning("Could not stop screen recording", exc_info=True)
        return None
    if not encoded:
        LOGGER.warning("Screen recording returned no data")
        return None
    LOGGER.info("Screen recording captured (%d base64 characters)", len(encoded))
    return base64.b64decode(encoded)


def attach_screenshot(driver: webdriver.Remote, name: str) -> None:
    """Attach the current screen to the Allure report."""
    try:
        allure.attach(
            driver.get_screenshot_as_png(),
            name=name,
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception:
        LOGGER.warning("Could not capture a screenshot", exc_info=True)


def attach_video(video: bytes, name: str) -> None:
    """Attach a recorded video to the Allure report."""
    allure.attach(video, name=name, attachment_type=allure.attachment_type.MP4)
    LOGGER.info("Video attached to Allure (%d bytes)", len(video))
