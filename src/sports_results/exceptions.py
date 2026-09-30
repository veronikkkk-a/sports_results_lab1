class SportsError(Exception):
    """Базовий виняток для системи обліку спортивних результатів."""


class AthleteNotFoundError(SportsError):
    """Викликається, коли спортсмена або результат не знайдено."""


class InvalidResultError(SportsError):
    """Викликається при введенні некоректного спортивного результату."""