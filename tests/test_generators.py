from src.generators import filter_by_currency, card_number_generator
import pytest

def test_card_number_generator():
    generator = card_number_generator(1, 5)
    assert next(generator) == "0000 0000 0000 0001"
    assert next(generator) == "0000 0000 0000 0002"
    assert next(generator) == "0000 0000 0000 0003"
    assert next(generator) == "0000 0000 0000 0004"
    assert next(generator) == "0000 0000 0000 0005"
    generator = card_number_generator(0, 0)
    assert next(generator) == "0000 0000 0000 0000"
    generator = card_number_generator()
    assert next(generator) == "Проверьте, что указаны входные данные"
