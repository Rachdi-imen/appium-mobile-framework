"""Unit tests for the cross-platform Locator (no device needed)."""

from dataclasses import FrozenInstanceError

import pytest

from core.enums import Platform
from core.locator import Locator


def test_locator_returns_android_strategy() -> None:
    locator = Locator(android=("id", "a"), ios=("name", "b"))
    assert locator.for_platform(Platform.ANDROID) == ("id", "a")


def test_locator_returns_ios_strategy() -> None:
    locator = Locator(android=("id", "a"), ios=("name", "b"))
    assert locator.for_platform(Platform.IOS) == ("name", "b")


def test_shared_locator_is_identical_on_both_platforms() -> None:
    locator = Locator.shared("accessibility id", "login")
    assert locator.for_platform(Platform.ANDROID) == locator.for_platform(Platform.IOS)


def test_locator_is_immutable() -> None:
    locator = Locator.shared("accessibility id", "login")
    with pytest.raises(FrozenInstanceError):
        locator.description = "changed"  # type: ignore[misc]