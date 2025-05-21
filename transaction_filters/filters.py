import re

def normalize_status(status):
    return status.strip().upper()

def filter_by_status(transactions, status):
    return [txn for txn in transactions if normalize_status(txn.get("status", "")) == normalize_status(status)]

def sort_transactions(transactions, ascending=True):
    return sorted(transactions, key=lambda x: x.get("date", ""), reverse=not ascending)

def filter_by_description(transactions, search_string):
    pattern = re.compile(search_string, re.IGNORECASE)
    return [txn for txn in transactions if pattern.search(txn.get("description", ""))]

def count_operations_by_category(transactions, categories):
    result = {}
    for category in categories:
        result[category] = sum(1 for txn in transactions if category.lower() in txn.get("description", "").lower())
    return result
