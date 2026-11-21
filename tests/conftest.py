"""Shared Pytest fixtures: configuration, driver lifecycle and failure artifacts."""

from collections.abc import Generator, Iterator

import pytest
from appium import webdriver

from config.settings import Settings, get_settings
from core.artifacts import (
    attach_screenshot,
    attach_video,
    start_video,
    stop_video,
)
from core.driver_factory import create_driver
from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.login_page import LoginPage
from pages.product_page import ProductPage

# Save the result of each test step to know whether the test failed, so we can take a screenshot and video on failure.
PHASE_REPORTS: pytest.StashKey[dict[str, pytest.TestReport]] = pytest.StashKey()


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(
    item: pytest.Item, call: pytest.CallInfo[None]
) -> Generator[None, pytest.TestReport, pytest.TestReport]:
    """Remember each phase result so fixtures can tell whether the test failed."""
    report = yield
    item.stash.setdefault(PHASE_REPORTS, {})[report.when] = report
    return report


def _test_failed(item: pytest.Item) -> bool:
    return any(rep.failed for rep in item.stash.get(PHASE_REPORTS, {}).values())


@pytest.fixture(scope="session")
def settings() -> Settings:
    """Validated configuration, loaded once per Pytest process."""
    return get_settings()


@pytest.fixture
def driver(
    settings: Settings, request: pytest.FixtureRequest
) -> Iterator[webdriver.Remote]:
    """Fresh Appium session per test. Keeps a screenshot and video on failure."""
    session = create_driver(settings, session_name=request.node.name)
    recording = start_video(session, settings) if settings.record_video else False
    try:
        yield session
    finally:
        failed = _test_failed(request.node)
        if failed:
            attach_screenshot(session, "failure-screenshot")
        video = stop_video(session) if recording else None
        if failed and video:
            attach_video(video, "failure-video")
        session.quit()


@pytest.fixture
def login_page(driver: webdriver.Remote) -> LoginPage:
    """Open the login screen with one product in the cart."""
    catalog = CatalogPage(driver)
    assert catalog.is_loaded()
    catalog.open_product("Sauce Labs Backpack")

    product = ProductPage(driver)
    assert product.is_loaded()
    product.add_to_cart()
    product.open_cart()

    cart = CartPage(driver)
    assert cart.is_loaded()
    cart.proceed_to_checkout()

    login = LoginPage(driver)
    assert login.is_loaded()
    return login
