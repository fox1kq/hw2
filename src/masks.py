def get_mask_number_card(card: str) -> str:
    """Функция, принимающая номер карты и возвращающая номер под маской,
    где видны первые 6 и последние 4 цифры."""
    new_card = "******".join([card[:6], card[12:]])
    card_under_mask = (
        new_card[:4] + " " + new_card[4:8] + " " + new_card[8:12] + " " + new_card[12:]
    )
    return card_under_mask


def get_mask_account(card: str) -> str:
    """Функция, принимающая номер карты и возвращающая номер под маской,
    где видны последние 4 цифры, а перед ними 2 звездочки"""
    return "**" + card[16:]
