"""Data-driven login tests: valid and invalid cases."""

import pytest
from appium import webdriver

from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from tests.data.login_cases import INVALID_CASES, VALID_CASES, LoginCase


def _sign_in(login_page: LoginPage, case: LoginCase) -> None:
    if case.saved_user:
        login_page.select_saved_user(case.saved_user)
        login_page.submit()
    else:
        login_page.login(case.username, case.password)


@pytest.mark.android
@pytest.mark.data_driven
@pytest.mark.parametrize("case", VALID_CASES, ids=lambda case: case.id)
def test_login_succeeds(
    driver: webdriver.Remote, login_page: LoginPage, case: LoginCase
) -> None:
    _sign_in(login_page, case)
    assert CheckoutPage(driver).is_loaded()


@pytest.mark.android
@pytest.mark.data_driven
@pytest.mark.parametrize("case", INVALID_CASES, ids=lambda case: case.id)
def test_login_is_rejected(login_page: LoginPage, case: LoginCase) -> None:
    _sign_in(login_page, case)
    assert case.error_field is not None
    assert login_page.error_message(case.error_field) == case.error_message
