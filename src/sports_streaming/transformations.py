from collections.abc import Iterable, Iterator
from sports_streaming.models import SportRecord

def normalize_names(records: Iterable[SportRecord]) -> Iterator[SportRecord]:
    """Нормалізація імен спортсменів та назв видів спорту (title case)."""
    for record in records:
        yield record._replace(
            athlete=record.athlete.title(),
            sport=record.sport.title(),
            category=record.category.title()
        )