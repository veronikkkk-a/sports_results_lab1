from collections.abc import Iterable, Iterator
from sports_streaming.models import SportRecord

def validate_sports_records(rows: Iterable[dict[str, str]]) -> Iterator[SportRecord]:
    """Потокова валідація та очищення записів спортивних результатів."""
    for row in rows:
        try:
            athlete = row["athlete"].strip()
            sport = row["sport"].strip()
            result = float(row["result"])
            category = row["category"].strip()
            timestamp = row["timestamp"].strip()
        except (ValueError, KeyError, TypeError):
            continue
        
        if not athlete or not sport or not category or not timestamp:
            continue
        if result < 0:
            continue
            
        yield SportRecord(
            athlete=athlete,
            sport=sport,
            result=result,
            category=category,
            timestamp=timestamp
        )

def filter_by_sport_and_category(
    records: Iterable[SportRecord],
    sport_filter: str | None = None,
    category_filter: str | None = None
) -> Iterator[SportRecord]:
    """Фільтрація записів за видом спорту та категорією."""
    for record in records:
        if sport_filter and record.sport.lower() != sport_filter.lower():
            continue
        if category_filter and record.category.lower() != category_filter.lower():
            continue
        yield record