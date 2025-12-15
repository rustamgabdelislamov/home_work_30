import stripe
from config.settings import STRIPE_API_KEY
stripe.api_key = STRIPE_API_KEY


def create_stripe_product(course_name):
    """Создает продукт в stripe"""

    product = stripe.Product.create(name=course_name)
    return product


def create_stripe_payment(amount,product_name):
    """Создает цену в stripe."""

    price = stripe.Price.create(
        currency="usd",
        unit_amount=int(amount),
        product_data={"name": product_name},
    )
    return price


def create_stripe_session(price):
    """Создает сессию на оплату в stripe."""
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")