"""Enumerations shared across the framework."""

from enum import StrEnum


class Platform(StrEnum):
    """Mobile platform under test."""

    ANDROID = "android"
    IOS = "ios"


class ExecutionMode(StrEnum):
    """Where the Appium session runs."""

    LOCAL = "local"
    BROWSERSTACK = "browserstack"
    SAUCELABS = "saucelabs"
