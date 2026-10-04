from collections.abc import Callable
from typing import Any
from sports_results.decorators import measure_time

@measure_time
def calculate_average_result(records: list[dict], sport_type: str | None = None) -> float:
    """Обчислення середнього результату (Generator Expression + Decorator)."""
    filtered = [r for r in records if r["sport_type"].lower() == sport_type.lower()] if sport_type else records
    if not filtered:
        return 0.0
    return sum(r["result"] for r in filtered) / len(filtered)

def find_best_athlete(records: list[dict]) -> dict | None:
    """Пошук найкращого результату за допомогою анонімної функції lambda."""
    if not records:
        return None
    return max(records, key=lambda r: r["result"])

def build_rating(records: list[dict], reverse: bool = True) -> list[dict]:
    """Сортування спортсменів та формування рейтингу."""
    return sorted(records, key=lambda r: r["result"], reverse=reverse)

def calculate_multi_average(*results: float) -> float:
    """Демонстрація *args для обчислення середнього значення довільної кількості результатів."""
    if not results:
        return 0.0
    return sum(results) / len(results)

def create_athlete_record(**kwargs: Any) -> dict:
    """Демонстрація **kwargs для створення запису з довільною кількістю полів."""
    return dict(kwargs)

def create_result_filter(min_result: float) -> Callable[[dict], bool]:
    """Closure (Замикання): створює функцію-фільтр із закріпленим пороговим значенням min_result."""
    def predicate(record: dict) -> bool:
        return record["result"] >= min_result
    return predicate