from sports_results.exceptions import AthleteNotFoundError, InvalidResultError
from sports_results.models import AthleteResult


def get_all_results(records: list[AthleteResult]) -> list[AthleteResult]:
    """Повертає список усіх спортивних результатів."""
    return records


def add_result(
    records: list[AthleteResult],
    name: str,
    sport_type: str,
    result: float,
    category: str,
) -> AthleteResult:
    """Додає новий спортивний результат."""
    if result <= 0:
        raise InvalidResultError("Спортивний результат повинен бути більше 0.")

    new_id = max([r.athlete_id for r in records], default=0) + 1
    new_record = AthleteResult(
        athlete_id=new_id,
        name=name,
        sport_type=sport_type,
        result=result,
        category=category,
    )
    records.append(new_record)
    return new_record


def find_by_sport(
    records: list[AthleteResult], sport_type: str
) -> list[AthleteResult]:
    """Шукає результати за видом спорту (без урахування регістру)."""
    s = sport_type.lower().strip()
    return [r for r in records if s in r.sport_type.lower()]


def get_best_result(
    records: list[AthleteResult], sport_type: str | None = None
) -> AthleteResult:
    """Визначає найкращий результат (максимальне значення) загалом або за видом спорту."""
    filtered = records
    if sport_type:
        filtered = find_by_sport(records, sport_type)

    if not filtered:
        raise AthleteNotFoundError("Результатів за вказаними критеріями не знайдено.")

    return max(filtered, key=lambda r: r.result)


def calculate_average_result(
    records: list[AthleteResult], sport_type: str | None = None
) -> float:
    """Обчислює середній результат загалом або за видом спорту."""
    filtered = records
    if sport_type:
        filtered = find_by_sport(records, sport_type)

    if not filtered:
        return 0.0

    total = sum(r.result for r in filtered)
    return total / len(filtered)


def get_rating(
    records: list[AthleteResult], sport_type: str | None = None
) -> list[AthleteResult]:
    """Формує рейтинг спортсменів (за спаданням результату)."""
    filtered = records
    if sport_type:
        filtered = find_by_sport(records, sport_type)

    return sorted(filtered, key=lambda r: r.result, reverse=True)