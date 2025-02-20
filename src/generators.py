from typing import Generator


def filter_by_currency(transactions: list[dict], currency: str) -> Generator:
    """Функция, которая фильтрует транзакции по заданной валюте."""
    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["code"] == currency:
            yield transaction


def transaction_descriptions(transactions: list[dict]) -> Generator:
    """Генератор, который возвращает описание каждой операции по очереди."""
    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(start: int, end: int) -> Generator:
    """Генератор, который выдает номера банковских карт в формате XXXX XXXX XXXX XXXX."""
    for card_number in range(start, end + 1):
        card_number_str = str(card_number)
        while len(card_number_str) < 16:
            card_number_str = "0" + card_number_str
        yield f"{card_number_str[:4]} {card_number_str[4:8]} {card_number_str[8:12]} {card_number_str[12:16]}"
