import requests
import os
from django.conf import settings


def process_payment(card_number, expiry_month, expiry_year, amount, currency, cvv):
    url = "https://api.sandbox.checkout.com/payments"
    headers = {
        "Authorization": f"Bearer {settings.CHECKOUT_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "source": {
            "type": "card",
            "number": card_number,
            "cvv": str(cvv),
            "expiry_month": int(expiry_month),
            "expiry_year": int(expiry_year),
        },
        "amount": amount,
        "currency": currency,
        "processing_channel_id": settings.CHECKOUT_PROCESSING_CHANNEL_ID,
        "reference": "ORD-5023-4E89",
        "metadata": {
            "udf1": "TEST123",
            "coupon_code": "NY2018",
            "partner_id": 123989,
        },
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()
