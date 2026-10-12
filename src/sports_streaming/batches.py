from collections.abc import Iterable, Iterator
from itertools import islice
from sports_streaming.models import SportRecord

def batched_records(iterable: Iterable[SportRecord], size: int) -> Iterator[list[SportRecord]]:
    """Потокова розбивка на батчі за допомогою islice."""
    iterator = iter(iterable)
    while True:
        batch = list(islice(iterator, size))
        if not batch:
            break
        yield batch