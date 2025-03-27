import json
import os


def load_financial_transactions(path_to_file):
    if not os.path.exists(path_to_file):
        return []

    with open(path_to_file, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        if isinstance(data, list):
            return data
        else:
            return []
