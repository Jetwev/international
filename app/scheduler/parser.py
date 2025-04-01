import json
import requests
from app.config import settings
from loguru import logger


def calculate_delivery_cost(weight_kg: float, price: float, usd_to_rub_rate: float) -> float:
    delivery_cost = (weight_kg * 0.5 + price * 0.01) * usd_to_rub_rate
    return round(delivery_cost, 2)


def get_rate() -> float | None:
    rate = None
    try:
        response = requests.get(settings.CURRENCY_URL)
        if response.status_code == 200:
            data = json.loads(response.text)
            rate = float(data['Valute']['USD']['Value'])
    except Exception as e:
        logger.error(f'Error while getting new rate from website: {e}')
    finally:
        return rate
