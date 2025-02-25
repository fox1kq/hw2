def get_mask_number_card(card: str) -> str:
    """Функция, принимающая номер карты и возвращающая номер под маской,
    где видны первые 6 и последние 4 цифры."""
    if len(card) == 16 and card.isdigit():
        new_card = "******".join([card[:6], card[12:]])
        card_under_mask = new_card[:4] + " " + new_card[4:8] + " " + new_card[8:12] + " " + new_card[12:]
        return card_under_mask
    else:
        return "Ошибка: Номер карты должен содержать только цифры и быть длиной 16 символов"


def get_mask_account(card: str) -> str:
    """Функция, принимающая номер счёта и возвращающая номер под маской,
    где видны последние 4 цифры, а перед ними 2 звездочки"""
    if len(card) == 20 and card.isdigit():
        return "**" + card[16:]
    else:
        return "Ошибка: Номер счёта должен содержать только цифры и быть длиной 20 символов"
