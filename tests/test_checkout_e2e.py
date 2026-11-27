"""Full purchase flow, from the catalog to the order confirmation."""

import pytest
from appium import webdriver

from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from pages.order_complete_page import OrderCompletePage
from pages.payment_page import PaymentPage
from pages.product_page import ProductPage
from pages.review_page import ReviewPage
from tests.data.checkout_data import CARD, SHIPPING_ADDRESS

PRODUCT = "Sauce Labs Backpack"
EXPECTED_TOTAL = "$ 35.98"


@pytest.mark.android
@pytest.mark.e2e
def test_checkout_e2e(driver: webdriver.Remote) -> None:
    catalog = CatalogPage(driver)
    assert catalog.is_loaded()
    catalog.open_product(PRODUCT)

    product = ProductPage(driver)
    assert product.is_loaded()
    product.add_to_cart()
    assert product.cart_count() == 1
    product.open_cart()

    cart = CartPage(driver)
    assert cart.is_loaded()
    assert cart.item_titles() == [PRODUCT]
    cart.proceed_to_checkout()

    login = LoginPage(driver)
    assert login.is_loaded()
    login.select_saved_user("bod@example.com")
    login.submit()

    checkout = CheckoutPage(driver)
    assert checkout.is_loaded()
    checkout.fill_address(
        full_name=SHIPPING_ADDRESS.full_name,
        address_line_1=SHIPPING_ADDRESS.address_line_1,
        city=SHIPPING_ADDRESS.city,
        zip_code=SHIPPING_ADDRESS.zip_code,
        country=SHIPPING_ADDRESS.country,
    )
    checkout.go_to_payment()

    payment = PaymentPage(driver)
    assert payment.is_loaded()
    payment.fill_card(
        holder=CARD.holder,
        number=CARD.number,
        expiration=CARD.expiration,
        security_code=CARD.security_code,
    )
    payment.set_billing_same_as_shipping(True)
    payment.review_order()

    review = ReviewPage(driver)
    assert review.is_loaded()
    assert review.item_titles() == [PRODUCT]
    assert review.total() == EXPECTED_TOTAL
    review.place_order()

    complete = OrderCompletePage(driver)
    assert complete.is_loaded()
    assert complete.title() == "Checkout Complete"
    assert complete.thank_you_message() == "Thank you for your order"

    complete.continue_shopping()
    assert catalog.is_loaded()
