"""Appium driver factory: builds a session for local or cloud execution."""

import logging

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from pydantic import SecretStr

from config.settings import Settings, get_settings
from core.enums import ExecutionMode, Platform

LOGGER = logging.getLogger(__name__)

BUILD_NAME = "appium-mobile-framework"

type DriverOptions = UiAutomator2Options | XCUITestOptions


def create_driver(
    settings: Settings | None = None,
    session_name: str = "mobile-test",
) -> webdriver.Remote:
    """Create an Appium session for the configured platform and execution mode."""
    cfg = settings or get_settings()
    options = _build_options(cfg)

    if cfg.is_cloud:
        _apply_cloud_capabilities(options, cfg, session_name)

    LOGGER.info(
        "Starting %s session (%s) on %s",
        cfg.platform,
        cfg.execution_mode,
        cfg.remote_url,
    )
    driver = webdriver.Remote(command_executor=cfg.remote_url, options=options)
    driver.implicitly_wait(0)
    return driver


def _build_android_options(cfg: Settings) -> UiAutomator2Options:
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = cfg.android_device_name
    options.new_command_timeout = cfg.new_command_timeout
    options.auto_grant_permissions = True
    # accept any activity instead of waiting for the splash one.
    options.app_wait_activity = "*"
    if cfg.android_platform_version:
        options.platform_version = cfg.android_platform_version
    if not cfg.is_cloud:
        options.app = str(cfg.local_app_path)
    if cfg.android_udid:
        options.udid = cfg.android_udid
    return options


def _build_options(cfg: Settings) -> DriverOptions:
    match cfg.platform:
        case Platform.ANDROID:
            return _build_android_options(cfg)
        case Platform.IOS:
            return _build_ios_options(cfg)


def _build_ios_options(cfg: Settings) -> XCUITestOptions:
    options = XCUITestOptions()
    options.platform_name = "iOS"
    options.device_name = cfg.ios_device_name
    options.new_command_timeout = cfg.new_command_timeout
    if cfg.ios_platform_version:
        options.platform_version = cfg.ios_platform_version
    if not cfg.is_cloud:
        options.app = str(cfg.local_app_path)
    return options


def _apply_cloud_capabilities(
    options: DriverOptions, cfg: Settings, session_name: str
) -> None:
    """Add provider-specific capabilities. Credentials never go in the URL."""
    match cfg.execution_mode:
        case ExecutionMode.BROWSERSTACK:
            options.app = cfg.browserstack_app_url
            options.device_name = cfg.browserstack_device_name
            options.platform_version = cfg.browserstack_platform_version
            options.set_capability(
                "bstack:options",
                {
                    "userName": cfg.browserstack_username,
                    "accessKey": _secret(cfg.browserstack_access_key),
                    "projectName": BUILD_NAME,
                    "buildName": BUILD_NAME,
                    "sessionName": session_name,
                },
            )
        case ExecutionMode.SAUCELABS:
            options.app = cfg.saucelabs_app
            options.device_name = cfg.saucelabs_device_name
            options.platform_version = cfg.saucelabs_platform_version
            options.set_capability(
                "sauce:options",
                {
                    "username": cfg.saucelabs_username,
                    "accessKey": _secret(cfg.saucelabs_access_key),
                    "build": BUILD_NAME,
                    "name": session_name,
                },
            )
        case _:
            raise ValueError(f"Unsupported cloud mode: {cfg.execution_mode}")


def _secret(value: SecretStr | None) -> str:
    if value is None:
        raise ValueError("A required cloud access key is missing")
    return value.get_secret_value()
