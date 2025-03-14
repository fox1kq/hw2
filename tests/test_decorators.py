import pytest

from src.decorators import log


def test_add(capsys: pytest.CaptureFixture) -> None:
    @log()
    def add(a: int, b: int) -> int:
        return a + b

    result = add(1, 2)
    captured = capsys.readouterr()
    assert result == 3
    assert captured.out == "add ok\n"


def test_divide(capsys: pytest.CaptureFixture) -> None:
    @log()
    def divide(a: int, b: int) -> int | float:
        return a / b

    result = divide(10, 2)
    captured = capsys.readouterr()
    assert result == 5
    assert captured.out == "divide ok\n"


def test_divide_by_zero(capsys: pytest.CaptureFixture) -> None:
    @log()
    def divide(a: int, b: int) -> int | float:
        return a / b

    result = divide(10, 0)
    captured = capsys.readouterr()
    assert result is None
    assert captured.out == "divide error: division by zero. Inputs: (10, 0), {}\n"


def test_raise_error(capsys: pytest.CaptureFixture) -> None:
    @log()
    def raise_error() -> None:
        raise ValueError("This is an error")

    result = raise_error()
    captured = capsys.readouterr()
    assert result is None
    assert captured.out == "raise_error error: This is an error. Inputs: (), {}\n"
