from src.reading import reading_from_csv, reading_from_excel


def test_reading_from_csv():
    assert reading_from_csv(r"C:\Users\Padusev.D\PycharmProjects\hw2\data\transactions.csv")[0] == {
        "id": "650703",
        "state": "EXECUTED",
        "date": "2023-09-05T11:30:32Z",
        "amount": "16210",
        "currency_name": "Sol",
        "currency_code": "PEN",
        "from": "Счет 58803664561298323391",
        "to": "Счет 39745660563456619397",
        "description": "Перевод организации",
    }


def test_reading_from_excel():
    assert reading_from_excel(r"C:\Users\Padusev.D\PycharmProjects\hw2\data\transactions_excel.xlsx")[0] == {
        "id": 650703.0,
        "state": "EXECUTED",
        "date": "2023-09-05T11:30:32Z",
        "amount": 16210.0,
        "currency_name": "Sol",
        "currency_code": "PEN",
        "from": "Счет 58803664561298323391",
        "to": "Счет 39745660563456619397",
        "description": "Перевод организации",
    }
