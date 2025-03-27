import requests
import os
from dotenv import load_dotenv

load_dotenv()

payload = {}
headers = {"apikey": os.getenv("API_KEY")}


def get_exchange_rate(transaction: dict) -> float:
    """Функция, которая принимает на вход транзакцию и возвращает сумму транзакции"""

    if transaction["operationAmount"]["currency"]["code"] == "RUB":
        return float(transaction["operationAmount"]["amount"])
    elif transaction["operationAmount"]["currency"]["code"] == "USD":
        amount = transaction["operationAmount"]["amount"]
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount={amount}"
        response = requests.get(url, headers=headers, data=payload)
        data = response.json()
        return float(data["result"])
    elif transaction["operationAmount"]["currency"]["code"] == "EUR":
        amount = transaction["operationAmount"]["amount"]
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=EUR&amount={amount}"
        response = requests.get(url, headers=headers, data=payload)
        data = response.json()
        return float(data["result"])
