"""Catalog to product navigation."""

import pytest
from appium import webdriver

from pages.catalog_page import CatalogPage
from pages.product_page import ProductPage


@pytest.mark.android
@pytest.mark.e2e
def test_open_product_from_catalog(driver: webdriver.Remote) -> None:
    catalog = CatalogPage(driver)
    assert catalog.is_loaded()

    catalog.open_product("Sauce Labs Backpack")

    product = ProductPage(driver)
    assert product.is_loaded()
    assert product.title() == "Sauce Labs Backpack"
    assert product.price() == "$ 29.99"