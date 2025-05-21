from transaction_filters.loader import load_json, load_csv, load_xlsx
from transaction_filters.filters import (
    filter_by_description,
    count_operations_by_category,
    filter_by_status,
    sort_transactions,
    normalize_status
)
from collections import Counter


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Пользователь: ").strip()
    file_path = r"D:\PythonProjects\hw2\data\operations.json"  # по умолчанию

    if choice == "1":
        transactions = load_json(file_path)
        print("Для обработки выбран JSON-файл.")
    elif choice == "2":
        transactions = load_csv("data.csv")
        print("Для обработки выбран CSV-файл.")
    elif choice == "3":
        transactions = load_xlsx("data.xlsx")
        print("Для обработки выбран XLSX-файл.")
    else:
        print("Неверный выбор. Завершение работы.")
        return


    available_statuses = {"EXECUTED", "CANCELED", "PENDING"}

    while True:
        status_input = input("Введите статус (EXECUTED, CANCELED, PENDING): ")
        if normalize_status(status_input) in available_statuses:
            break
        print(f'Статус операции "{status_input}" недоступен.')

    transactions = filter_by_status(transactions, status_input)
    print(f'Операции отфильтрованы по статусу "{normalize_status(status_input)}"')

    sort_answer = input("Отсортировать операции по дате? Да/Нет: ").strip().lower()
    if sort_answer == "да":
        order = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()
        ascending = order == "по возрастанию"
        transactions = sort_transactions(transactions, ascending)

    currency_answer = input("Выводить только рублевые тразакции? Да/Нет: ").strip().lower()
    if currency_answer == "да":
        transactions = [txn for txn in transactions if "руб" in str(txn.get("amount", "")).lower()]

    desc_filter = input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет: ").strip().lower()
    if desc_filter == "да":
        word = input("Введите слово для поиска: ").strip()
        transactions = filter_by_description(transactions, word)

    count_answer = input("Посчитать количество операций по категориям? Да/Нет: ").strip().lower()
    if count_answer == "да":
        category_counter = count_operations_by_category(transactions)
        print("Количество операций по категориям:")
        for category, count in category_counter.items():
            print(f"{category}: {count}")

    print("\nРаспечатываю итоговый список транзакций...")
    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print(f"Всего банковских операций в выборке: {len(transactions)}\n")
        for txn in transactions:
            print(f"{txn.get('date')} {txn.get('description')}")
            print(txn.get('from', ''), "->", txn.get('to', ''))
            print(f"Сумма: {txn.get('amount')}\n")


if __name__ == "__main__":
    main()
