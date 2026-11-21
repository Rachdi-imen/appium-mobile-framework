"""Cross-platform locator: one declaration, one strategy per platform."""

from dataclasses import dataclass
from typing import Self

from core.enums import Platform

type LocatorTuple = tuple[str, str]


@dataclass(frozen=True, slots=True)
class Locator:
    """Where to find an element on Android and on iOS."""

    android: LocatorTuple
    ios: LocatorTuple
    description: str = ""

    @classmethod
    def shared(cls, by: str, value: str, description: str = "") -> Self:
        """Same strategy and value on both platforms (e.g. an accessibility id)."""
        return cls(android=(by, value), ios=(by, value), description=description)

    def for_platform(self, platform: Platform) -> LocatorTuple:
        """Return the (strategy, value) pair for the given platform."""
        return self.android if platform is Platform.ANDROID else self.ios