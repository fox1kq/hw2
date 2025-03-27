from src.utils import load_financial_transactions


def test_load_financial_transactions():
    assert load_financial_transactions("data/financial_transactions.json") == []
