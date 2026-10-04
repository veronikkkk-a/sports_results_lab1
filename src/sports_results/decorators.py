from functools import wraps
from time import perf_counter
from typing import Callable, Any

def measure_time(func: Callable[..., Any]) -> Callable[..., Any]:
    """Декоратор для вимірювання та виведення часу виконання функції."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = perf_counter()
        result = func(*args, **kwargs)
        elapsed = perf_counter() - start_time
        print(f"[BENCHMARK] {func.__name__}: {elapsed:.8f} s")
        return result
    return wrapper