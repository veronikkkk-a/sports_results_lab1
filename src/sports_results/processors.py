from collections import Counter, defaultdict, deque
from typing import Any

def get_unique_sports(records: list[dict]) -> set[str]:
    """Set Comprehension: повертає множину унікальних видів спорту."""
    return {r["sport_type"] for r in records}

def create_athlete_index(records: list[dict]) -> dict[int, dict]:
    """Dict Comprehension: створює швидкий словник-індекс за ID."""
    return {r["id"]: r for r in records}

def group_by_sport(records: list[dict]) -> dict[str, list[dict]]:
    """Групування спортсменів за видами спорту з використанням defaultdict."""
    grouped = defaultdict(list)
    for r in records:
        grouped[r["sport_type"]].append(r)
    return dict(grouped)

def count_athletes_by_sport(records: list[dict]) -> Counter:
    """Підрахунок кількості спортсменів у кожному виді спорту за допомогою Counter."""
    return Counter(r["sport_type"] for r in records)

def track_recent_results(records: list[dict], maxlen: int = 3) -> deque:
    """Використання deque для ведення історії останніх операцій/записів."""
    history = deque(maxlen=maxlen)
    for r in records:
        history.append(r)
    return history