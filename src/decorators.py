from typing import Any, Optional


def log(filename: Optional[str] = None) -> Any:
    """Декоратор, который логирует начало и конец выполнения функции, а также ее результаты или возникшие ошибки"""

    def decorator(func: Any) -> Any:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                log_end = f"{func.__name__} ok"
            except Exception as e:
                log_end = f"{func.__name__} error: {e}. Inputs: {args}, {kwargs}"
                result = None

            if filename:
                with open(filename, "a") as file:
                    file.write(log_end)
            else:
                print(log_end)

            return result

        return wrapper

    return decorator
