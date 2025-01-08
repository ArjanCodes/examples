import random
import struct

with open("data.bin", "wb") as f:
    for _ in range(10_000_000):  # 10 million integers
        f.write(struct.pack("<i", random.randint(-1_000_000, 1_000_000)))
