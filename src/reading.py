import csv
from typing import Any
import pandas as pd


def reading_from_csv(path: str) -> Any:
    with open(path, encoding="utf8") as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            print(row)


def reading_from_excel(path:str) -> Any:
    df = pd.read_excel(path)
    return df
