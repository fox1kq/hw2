from src.masks import get_mask_account, get_mask_number_card


def mask_account_card(card: str) -> str:
    """Функция, принимающая номер карты и тип, возвращающая номер
    под маской, где видны первые 6 и последние 4 цифры."""
    data_of_card = card.split()
    if data_of_card[0] == "Счет":
        answer = get_mask_account(data_of_card[1])
        if answer[2:].isdigit():
            return f"Счет {answer}"
        else:
            return answer
    else:
        count_of_values = len(data_of_card)
        index_of_number = count_of_values - 1
        number_of_card = data_of_card[index_of_number]
        value_of_issuer = " ".join(data_of_card[:index_of_number])
        final_number_card = get_mask_number_card(number_of_card)
        final_number_card_list = final_number_card.split()
        if final_number_card_list[0] == "Ошибка:":
            return f"{" ".join(final_number_card_list)}"
        else:
            return f"{value_of_issuer} {" ".join(final_number_card_list)}"


def get_date(user_date: str) -> str:
    """Функция, принимающая на вход строку с датой,
    которая возвращает её в формате ДД.ММ.ГГГГ"""
    try:
        if len(user_date) == 26:
            date = user_date[:10].split("-")
            date.reverse()
            answer = ".".join(date)
            answer_test = answer.replace(".", "")
            if answer_test.isdigit():
                return answer
            else:
                return "Ошибка: Неверный тип данных"
        else:
            return "Ошибка: Неверный тип данных"
    except TypeError:
        return "Ошибка: Неверный тип данных"
