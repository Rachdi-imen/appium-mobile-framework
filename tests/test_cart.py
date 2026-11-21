"""Add a product to the cart and go to checkout."""

import pytest
from appium import webdriver

from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.login_page import LoginPage
from pages.product_page import ProductPage


@pytest.mark.android
@pytest.mark.e2e
def test_add_to_cart_then_checkout_asks_for_login(driver: webdriver.Remote) -> None:
    catalog = CatalogPage(driver)
    assert catalog.is_loaded()
    catalog.open_product("Sauce Labs Backpack")

    product = ProductPage(driver)
    assert product.is_loaded()
    product.add_to_cart()
    assert product.cart_count() == 1

    product.open_cart()
    cart = CartPage(driver)
    assert cart.is_loaded()
    assert cart.item_titles() == ["Sauce Labs Backpack"]
    assert cart.total_price() == "$ 29.99"

    cart.proceed_to_checkout()
    assert LoginPage(driver).is_loaded()
