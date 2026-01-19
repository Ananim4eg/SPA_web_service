import requests
import stripe

from config.settings import STRIPE_API_KEY, CURRENCY_API_KEY

stripe.api_key = STRIPE_API_KEY


def convert_rub_to_usd(amount_rub: float) -> int:
    """Перевод валюты из рублей в доллары"""

    url = f'https://api.currencyapi.com/v3/latest?apikey={CURRENCY_API_KEY}&currencies=USD&base_currency=RUB'

    response = requests.get(url)

    rate = response.json()['data']['USD']['value']

    return int(round(amount_rub * rate, 2))


def create_product_price_in_stripe(product_name: str, product_price: int) -> str:
    """Создание цены продукта в сервисе Strip3"""

    price = stripe.Price.create(
        currency="usd",
        unit_amount=product_price * 100,
        product_data={"name": f"{product_name}"},
    )

    return price['id']


def create_payment_link_in_stripe(price_id: str) -> str:
    """Создание ссылки для оплаты продукта в сервисе Strip3"""

    payment_link = stripe.PaymentLink.create(
        after_completion={
            "redirect": {"url": "http://127.0.0.1:8000"},
            "type": "redirect"
        },
        line_items=[{"price": f"{price_id}", "quantity": 1}],
    )

    return payment_link['url']
