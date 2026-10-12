from collections.abc import Iterable
from sports_streaming.models import SportRecord

def streaming_average_result(records: Iterable[SportRecord]) -> float:
    """Потокове обчислення середнього результату без матеріалізації."""
    total = 0.0
    count = 0
    for record in records:
        total += record.result
        count += 1
    return total / count if count > 0 else 0.0

def find_best_result(records: Iterable[SportRecord]) -> SportRecord | None:
    """Визначення найкращого результату у потоці."""
    best = None
    for record in records:
        if best is None or record.result > best.result:
            best = record
    return best

def streaming_min_max(records: Iterable[SportRecord]) -> tuple[float | None, float | None]:
    """Визначення мінімального та максимального результатів."""
    minimum = None
    maximum = None
    for record in records:
        val = record.result
        if minimum is None or val < minimum:
            minimum = val
        if maximum is None or val > maximum:
            maximum = val
    return minimum, maximum