import datetime
import logging
import os
from typing import Dict, List, Union
import requests
import json
from datetime import datetime as dt
from decorators import log
from masks import get_mask_number_card
from widget import get_date as widget_format_date
from external_api import get_exchange_rate
from processing import sort_by_date
from utils import load_financial_transactions
from generators import filter_by_currency

# Настройка логирования
LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, 'views.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Загрузка пользовательских настроек
try:
    with open(os.path.join(os.path.dirname(__file__), 'user_settings.json'), 'r', encoding='utf-8') as f:
        USER_SETTINGS = json.load(f)
except FileNotFoundError:
    logger.error("Файл user_settings.json не найден")
    USER_SETTINGS = {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    }

# API ключи (должны быть в конфигурации или переменных окружения)
CURRENCY_API_KEY = "YOUR_CURRENCY_API_KEY"
STOCK_API_KEY = "YOUR_STOCK_API_KEY"


@log
def get_greeting(time_str: str) -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    try:
        time = dt.strptime(time_str, "%Y-%m-%d %H:%M:%S").time()
        if 5 <= time.hour < 12:
            return "Доброе утро"
        elif 12 <= time.hour < 17:
            return "Добрый день"
        elif 17 <= time.hour < 23:
            return "Добрый вечер"
        return "Доброй ночи"
    except ValueError as e:
        logger.error(f"Ошибка формата времени: {e}")
        return "Добрый день"


@log
def get_currency_rates() -> List[Dict[str, Union[str, float]]]:
    """Получает текущие курсы валют из API."""
    try:
        rates = []
        for currency in USER_SETTINGS["user_currencies"]:
            rate = get_exchange_rate(currency)
            if rate is not None:
                rates.append({"currency": currency, "rate": round(rate, 2)})
        return rates
    except Exception as e:
        logger.error(f"Ошибка при получении курсов валют: {e}")
        return []


@log
def get_stock_prices() -> List[Dict[str, Union[str, float]]]:
    """Получает текущие цены акций из API."""
    stocks = []
    for stock in USER_SETTINGS["user_stocks"]:
        try:
            url = "https://www.alphavantage.co/query"
            params = {
                "function": "GLOBAL_QUOTE",
                "symbol": stock,
                "apikey": STOCK_API_KEY
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            price = float(data["Global Quote"]["05. price"])
            stocks.append({"stock": stock, "price": price})
        except Exception as e:
            logger.error(f"Ошибка при получении цены акции {stock}: {e}")
    return stocks


@log
def get_transactions_for_period(start_date: str, end_date: str) -> List[Dict]:
    """Получает транзакции за указанный период."""
    try:
        transactions = load_financial_transactions()
        filtered = [
            t for t in transactions
            if start_date <= t["date"] <= end_date
        ]
        return sort_by_date(filtered)
    except Exception as e:
        logger.error(f"Ошибка при загрузке транзакций: {e}")
        return []


@log
def get_card_summary(card_transactions: List[Dict]) -> Dict:
    """Считает статистику по карте."""
    try:
        expenses = [t["amount"] for t in card_transactions if t.get("amount", 0) < 0]
        total = abs(sum(expenses))
        cashback = total // 100

        top_transactions = sorted(
            card_transactions,
            key=lambda x: abs(x.get("amount", 0)),
            reverse=True
        )[:5]

        return {
            "total": round(total),
            "cashback": cashback,
            "top_transactions": [
                {
                    "date": widget_format_date(t["date"]),
                    "amount": abs(t["amount"]),
                    "category": t["category"],
                    "description": t["description"]
                } for t in top_transactions
            ]
        }
    except Exception as e:
        logger.error(f"Ошибка при расчете статистики по карте: {e}")
        return {"total": 0, "cashback": 0, "top_transactions": []}


@log
def get_main_page_data(date_time: str) -> Dict:
    """Генерирует данные для главной страницы."""
    try:
        greeting = get_greeting(date_time)
        date = date_time.split()[0]
        year, month, _ = date.split('-')
        start_date = f"{year}-{month}-01"

        transactions = get_transactions_for_period(start_date, date)

        # Группировка по картам
        cards = {}
        for t in transactions:
            if "card_number" in t:
                card = get_mask_number_card(t["card_number"])
                if card not in cards:
                    cards[card] = []
                cards[card].append(t)

        cards_summary = {}
        for card, card_trans in cards.items():
            cards_summary[card] = get_card_summary(card_trans)

        return {
            "greeting": greeting,
            "cards": cards_summary,
            "currency_rates": get_currency_rates(),
            "stock_prices": get_stock_prices()
        }
    except Exception as e:
        logger.error(f"Ошибка при генерации данных главной страницы: {e}")
        return {
            "greeting": "Добрый день",
            "cards": {},
            "currency_rates": [],
            "stock_prices": []
        }


@log
def get_expenses_analysis(transactions: List[Dict]) -> Dict:
    """Анализирует расходы по категориям."""
    try:
        expenses = [t for t in transactions if t.get("amount", 0) < 0]

        # Группировка по категориям
        categories = {}
        for t in expenses:
            category = t["category"]
            amount = abs(t["amount"])
            categories[category] = categories.get(category, 0) + amount

        # Сортировка и разделение на основные и остальные
        sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
        main_categories = [{"category": k, "amount": round(v)} for k, v in sorted_categories[:7]]
        other_amount = sum(v for k, v in sorted_categories[7:])

        if other_amount > 0:
            main_categories.append({"category": "Остальное", "amount": round(other_amount)})

        # Переводы и наличные
        transfers_cash = []
        for category in ["Переводы", "Наличные"]:
            amount = sum(
                abs(t["amount"])
                for t in expenses
                if t["category"] == category
            )
            if amount > 0:
                transfers_cash.append({"category": category, "amount": round(amount)})

        return {
            "total_amount": round(sum(abs(t["amount"]) for t in expenses)),
            "main": main_categories,
            "transfers_and_cash": transfers_cash
        }
    except Exception as e:
        logger.error(f"Ошибка при анализе расходов: {e}")
        return {
            "total_amount": 0,
            "main": [],
            "transfers_and_cash": []
        }


@log
def get_income_analysis(transactions: List[Dict]) -> Dict:
    """Анализирует поступления по категориям."""
    try:
        income = [t for t in transactions if t.get("amount", 0) > 0]

        # Группировка по категориям
        categories = {}
        for t in income:
            category = t["category"]
            amount = t["amount"]
            categories[category] = categories.get(category, 0) + amount

        # Сортировка
        sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)

        return {
            "total_amount": round(sum(t["amount"] for t in income)),
            "main": [{"category": k, "amount": round(v)} for k, v in sorted_categories]
        }
    except Exception as e:
        logger.error(f"Ошибка при анализе поступлений: {e}")
        return {
            "total_amount": 0,
            "main": []
        }


@log
def get_events_page_data(date_time: str, period: str = "M") -> Dict:
    """Генерирует данные для страницы событий."""
    try:
        date = date_time.split()[0]
        year, month, day = map(int, date.split('-'))

        if period == "W":
            # Неделя
            start_date = dt(year, month, day) - datetime.timedelta(days=dt(year, month, day).weekday())
            start_date = start_date.strftime("%Y-%m-%d")
        elif period == "M":
            # Месяц
            start_date = f"{year}-{month:02d}-01"
        elif period == "Y":
            # Год
            start_date = f"{year}-01-01"
        elif period == "ALL":
            # Все данные
            start_date = "1970-01-01"
        else:
            start_date = f"{year}-{month:02d}-01"

        transactions = get_transactions_for_period(start_date, date)

        return {
            "expenses": get_expenses_analysis(transactions),
            "income": get_income_analysis(transactions),
            "currency_rates": get_currency_rates(),
            "stock_prices": get_stock_prices()
        }
    except Exception as e:
        logger.error(f"Ошибка при генерации данных страницы событий: {e}")
        return {
            "expenses": {"total_amount": 0, "main": [], "transfers_and_cash": []},
            "income": {"total_amount": 0, "main": []},
            "currency_rates": [],
            "stock_prices": []
        }