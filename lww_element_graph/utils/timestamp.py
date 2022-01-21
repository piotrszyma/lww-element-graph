import time


def timestamp_now() -> int:
    return time.monotonic_ns()
