import logging

# Основная конфигурация logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=r"D:\PythonProjects\hw2\logs\masks.log",
    filemode="w",
    encoding="utf-8",
)


mask_card_logger = logging.getLogger("mask_card")
mask_account_logger = logging.getLogger("mask_account")


def get_mask_number_card(card: str) -> str:
    """Функция, принимающая номер карты и возвращающая номер под маской,
    где видны первые 6 и последние 4 цифры."""

    mask_card_logger.info("Начало выполнения функции")
    if len(card) == 16 and card.isdigit():
        new_card = "******".join([card[:6], card[12:]])
        card_under_mask = new_card[:4] + " " + new_card[4:8] + " " + new_card[8:12] + " " + new_card[12:]
        mask_card_logger.info("Успешное выполнение функции")
        return card_under_mask
    else:
        mask_card_logger.warning("Неверные входные данные, ошибка")
        return "Ошибка: Номер карты должен содержать только цифры и быть длиной 16 символов"


def get_mask_account(card: str) -> str:
    """Функция, принимающая номер счёта и возвращающая номер под маской,
    где видны последние 4 цифры, а перед ними 2 звездочки"""

    mask_account_logger.info("Начало выполнения функции")
    if len(card) == 20 and card.isdigit():
        mask_card_logger.info("Успешное выполнение функции")
        return "**" + card[16:]
    else:
        mask_card_logger.warning("Неверные входные данные, ошибка")
        return "Ошибка: Номер счёта должен содержать только цифры и быть длиной 20 символов"
