import csv
from collections.abc import Iterable, Iterator

def parse_csv_rows(lines: Iterable[str]) -> Iterator[dict[str, str]]:
    """Парсинг рядків CSV у словники через csv.DictReader (lazy)."""
    reader = csv.DictReader(lines)
    yield from reader