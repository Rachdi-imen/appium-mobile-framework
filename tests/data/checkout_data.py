"""Checkout test data"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ShippingAddress:
    full_name: str
    address_line_1: str
    city: str
    zip_code: str
    country: str


@dataclass(frozen=True)
class PaymentCard:
    holder: str
    number: str
    expiration: str
    security_code: str


SHIPPING_ADDRESS = ShippingAddress(
    full_name="Test User",
    address_line_1="1 Test Street",
    city="Testville",
    zip_code="12345",
    country="Testland",
)

CARD = PaymentCard(
    holder="Test User",
    number="123456789632",
    expiration="12/30",
    security_code="123",
)
