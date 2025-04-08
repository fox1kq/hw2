import csv
from typing import Any

import pandas as pd


def reading_from_csv(path: str) -> Any:
    """Функция для считывания финансовых операций из CSV"""

    transactions_list = []

    with open(path, encoding="utf8") as file:
        reader = csv.reader(file, delimiter=";")
        next(reader)
        for row in reader:
            transactions = {
                "id": row[0],
                "state": row[1],
                "date": row[2],
                "amount": row[3],
                "currency_name": row[4],
                "currency_code": row[5],
                "from": row[6],
                "to": row[7],
                "description": row[8],
            }
            transactions_list.append(transactions)

    return transactions_list


def reading_from_excel(path: str) -> Any:
    """Функция для считывания финансовых операций из Excel"""

    df = pd.read_excel(path)
    transactions_list = df.to_dict(orient="records")
    return transactions_list
