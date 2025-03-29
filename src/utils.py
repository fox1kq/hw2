import json
import logging
import os

# Основная конфигурация logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=r"D:\PythonProjects\hw2\logs\utils.log",
    filemode="w",
    encoding="utf-8",
)


load_financial_transactions_logger = logging.getLogger("load_financial_transactions")


def load_financial_transactions(path_to_file):
    load_financial_transactions_logger.info("Начало выполнения функции")

    if not os.path.exists(path_to_file):
        load_financial_transactions_logger.warning("Файл не найден")
        return []

    with open(path_to_file, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

        if isinstance(data, list):
            load_financial_transactions_logger.info("Успешное выполнение")
            return data

        else:
            load_financial_transactions_logger.warning("Файл не содержит списка")
            return []
