import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.mark.parametrize(
    "list_of_operation, value_of_state, returned",
    [
        (
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
            "EXECUTED",
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
        ),
        (
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
            "CANCELED",
            [
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
        ),
        ([], "", []),
        ([], "EXECUTED", []),
        (
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
            "",
            [],
        ),
        (
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
            "PENDING",
            [],
        ),
        ([{"id": 1, "state": 123, "date": "2022-01-01T00:00:00"}], "123", []),
        (
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
            "executed",
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
        ),
    ],
)
def test_filter_by_state(list_of_operation: list, value_of_state: str, returned: list) -> None:
    assert filter_by_state(list_of_operation, value_of_state) == returned


@pytest.mark.parametrize(
    "list_of_operation, reverse, list_after_sort",
    [
        (
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
            True,
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
        ),
        ([], True, []),
        (
            [
                {"id": 1, "state": "EXECUTED", "date": "2022-01-01T12:00:00"},
                {"id": 2, "state": "EXECUTED", "date": "2021-06-15T08:30:00"},
                {"id": 3, "state": "CANCELED", "date": "2023-03-10T14:15:00"},
            ],
            False,
            [
                {"id": 2, "state": "EXECUTED", "date": "2021-06-15T08:30:00"},
                {"id": 1, "state": "EXECUTED", "date": "2022-01-01T12:00:00"},
                {"id": 3, "state": "CANCELED", "date": "2023-03-10T14:15:00"},
            ],
        ),
        (
            [{"id": 1, "state": "EXECUTED", "date": "2022-01-01T12:00:00"}],
            False,
            [{"id": 1, "state": "EXECUTED", "date": "2022-01-01T12:00:00"}],
        ),
        (
            [
                {"id": 1, "state": "EXECUTED", "date": "2022-01-01T12:00:00"},
                {"id": 2, "state": "EXECUTED", "date": "2022-01-01T12:00:00"},
                {"id": 3, "state": "CANCELED", "date": "2022-01-01T12:00:00"},
            ],
            True,
            [
                {"id": 1, "state": "EXECUTED", "date": "2022-01-01T12:00:00"},
                {"id": 2, "state": "EXECUTED", "date": "2022-01-01T12:00:00"},
                {"id": 3, "state": "CANCELED", "date": "2022-01-01T12:00:00"},
            ],
        ),
        (
            [
                {"id": 1, "state": "EXECUTED", "date": "2050-07-15T10:00:00"},
                {"id": 2, "state": "CANCELED", "date": "2049-06-01T08:00:00"},
            ],
            False,
            [
                {"id": 2, "state": "CANCELED", "date": "2049-06-01T08:00:00"},
                {"id": 1, "state": "EXECUTED", "date": "2050-07-15T10:00:00"},
            ],
        ),
        (
            [
                {"id": 1, "state": "EXECUTED", "date": "2022-01-01T12:00:00"},
                {"id": 2, "state": "EXECUTED"},  # У этого элемента нет даты
                {"id": 3, "state": "CANCELED", "date": "2023-03-10T14:15:00"},
            ],
            True,
            "Ошибка: Проверьте данные",
        ),
    ],
)
def test_sort_by_date(list_of_operation: list, reverse: bool, list_after_sort: list) -> None:
    assert sort_by_date(list_of_operation, reverse) == list_after_sort
