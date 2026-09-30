from dataclasses import dataclass


@dataclass
class AthleteResult:
    athlete_id: int
    name: str
    sport_type: str
    result: float  # Бали, секунди або метри
    category: str  # Наприклад: "Юніори", "Дорослі", "Професіонали"