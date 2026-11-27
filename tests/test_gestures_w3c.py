"""W3C Actions: drawing a shape on the Drawing screen."""

import pytest
from appium import webdriver

from pages.catalog_page import CatalogPage
from pages.drawing_page import DrawingPage
from pages.menu_page import MenuPage


@pytest.mark.android
@pytest.mark.gestures
def test_draw_square_and_save(driver: webdriver.Remote) -> None:
    catalog = CatalogPage(driver)
    assert catalog.is_loaded()

    MenuPage(driver).go_to("Drawing")

    drawing = DrawingPage(driver)
    assert drawing.is_loaded()
    drawing.draw_square()
    drawing.save()

    assert drawing.save_message() == "Drawing saved successfully to gallery"
    drawing.confirm_save()
