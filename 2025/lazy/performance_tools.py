import psutil
import os
from functools import wraps
import time

def measure_performance(func):
    """Measure execution time and memory usage."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        process = psutil.Process(os.getpid())
        mem_before: float = process.memory_info().rss / 1024**2
        start: float = time.time()

        result = func(*args, **kwargs)

        duration: float = time.time() - start
        mem_after: float = process.memory_info().rss / 1024**2
        print(f"⏱ {func.__name__} took {duration:.2f}s, "
              f"used {mem_after - mem_before:.1f} MB\n")
        return result
    return wrapper