import time
import gzip
import bz2
import compression.zstd as zstd  # New in Python 3.14

from typing import Callable

type CompressionFunction = Callable[[bytes], bytes]


def benchmark_compression(
    name: str,
    compress_fn: CompressionFunction,
    decompress_fn: CompressionFunction,
    data: bytes
) -> None:
    """Benchmark compression and decompression performance."""
    # Compress
    start = time.perf_counter()
    compressed: bytes = compress_fn(data)
    compress_time: float = time.perf_counter() - start

    # Decompress
    start = time.perf_counter()
    decompressed: bytes = decompress_fn(compressed)
    decompress_time: float = time.perf_counter() - start

    assert decompressed == data, f"{name} decompressed data mismatch!"

    print(
        f"{name:>6} | Size: {len(compressed):7} bytes | "
        f"Compress: {compress_time * 1000:7.2f} ms | "
        f"Decompress: {decompress_time * 1000:7.2f} ms"
    )


def main() -> None:
    data: bytes = (
        b"ArjanCodes is the best Python channel on YouTube!" * 50_000
    )

    print("== Compression Benchmark ==")

    benchmark_compression(
        "zstd",
        compress_fn=zstd.compress,
        decompress_fn=zstd.decompress,
        data=data,
    )

    benchmark_compression(
        "gzip",
        compress_fn=gzip.compress,
        decompress_fn=gzip.decompress,
        data=data,
    )

    benchmark_compression(
        "bz2",
        compress_fn=bz2.compress,
        decompress_fn=bz2.decompress,
        data=data,
    )


if __name__ == "__main__":
    main()