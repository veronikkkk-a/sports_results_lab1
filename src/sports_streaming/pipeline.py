from pathlib import Path
from sports_streaming.readers import read_lines
from sports_streaming.parsers import parse_csv_rows
from sports_streaming.filters import validate_sports_records, filter_by_sport_and_category
from sports_streaming.transformations import normalize_names

def build_pipeline(
    path: Path,
    sport: str | None = None,
    category: str | None = None
):
    """Побудова ледачого конвеєра обробки спортивних результатів."""
    lines = read_lines(path)
    rows = parse_csv_rows(lines)
    valid = validate_sports_records(rows)
    normalized = normalize_names(valid)
    filtered = filter_by_sport_and_category(normalized, sport=sport, category_filter=category)
    return filtered