import gc
import time
import cProfile
import pstats
from typing import Any


# Function to simulate a more complex, memory-intensive workload
def create_large_cycle(n: int):
    objects: list[tuple[dict[str, Any], dict[str, Any], dict[str, Any]]] = []
    for _ in range(n):
        a: dict[str, Any] = {}
        b: dict[str, Any] = {}
        c: dict[str, Any] = {}
        a["b"] = b
        b["c"] = c
        c["a"] = a
        objects.append((a, b, c))
    return objects


def measure_gc_efficiency(n: int) -> float:
    print(f"Creating {n} cyclic references...")
    objects = create_large_cycle(n)

    # Clear the references to allow garbage collection
    del objects

    print("Forcing garbage collection...")
    start_time = time.time()
    gc.collect()
    end_time = time.time()

    gc_time = end_time - start_time
    print(f"Garbage collection took {gc_time:.4f} seconds.")
    return gc_time


def main() -> None:
    N = 10**6
    print("Profiling garbage collection...")
    profiler = cProfile.Profile()
    profiler.enable()
    gc_time = measure_gc_efficiency(N)
    profiler.disable()

    # Print out the profiling results
    stats = pstats.Stats(profiler)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
    print(f"Garbage collection took {gc_time:.4f} seconds.")


# Test with a very large number of objects
if __name__ == "__main__":
    main()
