from unittest.mock import patch

from src.external_api import get_exchange_rate


@patch("requests.get")
def test_get_exchange_rate_rub(mock_get):
    mock_get.return_value.json.return_value = {"result": 31957.58}
    assert (
        get_exchange_rate(
            {
                "id": 441945886,
                "state": "EXECUTED",
                "date": "2019-08-26T10:50:58.294041",
                "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
                "description": "Перевод организации",
                "from": "Maestro 1596837868705199",
                "to": "Счет 64686473678894779589",
            }
        )
        == 31957.58
    )


@patch("requests.get")
def test_get_exchange_rate_usd(mock_get):
    mock_get.return_value.json.return_value = {"result": 689166.43}
    assert (
        get_exchange_rate(
            {
                "id": 41428829,
                "state": "EXECUTED",
                "date": "2019-07-03T18:35:29.512364",
                "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}},
                "description": "Перевод организации",
                "from": "MasterCard 7158300734726758",
                "to": "Счет 35383033474447895560",
            }
        )
        == 689166.43
    )
