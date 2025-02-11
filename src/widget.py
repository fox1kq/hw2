import masks


def mask_account_card(card: str) -> str:
    """Функция, принимающая номер карты и тип, возвращающая номер
    под маской, где видны первые 6 и последние 4 цифры."""
    data_of_card = card.split()
    if data_of_card[0] == "Счет":
        answer = masks.get_mask_account(data_of_card[1])
        return f"Счет {answer}"
    else:
        count_of_values = len(data_of_card)
        index_of_number = count_of_values - 1
        number_of_card = data_of_card[index_of_number]
        value_of_issuer = " ".join(data_of_card[:index_of_number])
        final_number_card = masks.get_mask_number_card(number_of_card)
        return f"{value_of_issuer} {final_number_card}"


def get_date(user_date: str) -> str:
    """Функция, принимающая на вход строку с датой,
    которая возвращает её в формате ДД.ММ.ГГГГ"""
    date = user_date[:10].split("-")
    date.reverse()
    answer = ".".join(date)
    return answer
