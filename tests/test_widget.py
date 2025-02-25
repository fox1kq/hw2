import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "card, card_under_mask",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Счет 7365410843013587430", "Ошибка: Номер счёта должен содержать только цифры и быть длиной 20 символов"),
        (
            "Visa Platinum 700079228960636",
            "Ошибка: Номер карты должен содержать только цифры и быть длиной 16 символов",
        ),
        ("1234a5678901234", "Ошибка: Номер карты должен содержать только цифры и быть длиной 16 символов"),
    ],
)
def test_mask_account_card(card: str, card_under_mask: str) -> None:
    assert mask_account_card(card) == card_under_mask


@pytest.mark.parametrize(
    "date, date_after_func",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("", "Ошибка: Неверный тип данных"),
        ("блаблабла", "Ошибка: Неверный тип данных"),
        ("2024-03-11", "Ошибка: Неверный тип данных"),
        ("abcd-ef-ghTij:kl:mn.opqrst", "Ошибка: Неверный тип данных"),
        ("2024/03/11T02:26:18.671407", "Ошибка: Неверный тип данных"),
        (None, "Ошибка: Неверный тип данных"),
    ],
)
def test_get_date(date: str, date_after_func: str) -> None:
    assert get_date(date) == date_after_func
