from __future__ import annotations

import time
from collections.abc import Iterator
from contextlib import contextmanager


@contextmanager
def time_recorder(timings: dict[str, float], key: str) -> Iterator[None]:
    start = time.perf_counter()
    try:
        yield
    finally:
        timings[key] = timings.get(key, 0.0) + (time.perf_counter() - start)
