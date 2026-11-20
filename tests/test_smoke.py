"""Minimal sanity check: the app launches and the driver fixture works."""

import pytest
from appium import webdriver

from config.settings import Settings


@pytest.mark.smoke
@pytest.mark.android
def test_app_launches(driver: webdriver.Remote, settings: Settings) -> None:
    assert driver.current_package == settings.android_app_package

def test_forced_failure(driver: webdriver.Remote) -> None:
    assert False, "Intentional failure to check Allure attachments"