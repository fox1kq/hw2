from typing import Union


def filter_by_state(list_of_operation: list, value_of_state: str) -> list:
    """Функция, которая принимает список словарей и возвращает словари, содержащие указанный ключ."""
    list_for_return = []
    for i in range(len(list_of_operation)):
        if list_of_operation[i]["state"] == value_of_state.upper():
            list_for_return.append(list_of_operation[i])
    return list_for_return


def sort_by_date(list_of_operation: list, reverse: bool = True) -> Union[list, str]:
    """Сортирует список словарей по дате"""
    try:
        return sorted(list_of_operation, key=lambda x: x["date"], reverse=reverse)
    except KeyError:
        return "Ошибка: Проверьте данные"
