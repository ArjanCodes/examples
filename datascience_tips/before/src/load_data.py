import gzip
import struct
from pathlib import Path

import numpy as np

DATA_DIR = (Path(__file__).parent / "../data").resolve()

ALLOWED_TYPES = {
    "UNSIGNED_BYTE": b"\x08",
    "SIGNED_BYTE": b"\x09",
    "SHORT": b"\x0B",
    "INT": b"\x0C",
    "SINGLE": b"\x0D",
    "DOUBLE": b"\x0E",
}


def load_test_data():
    with gzip.open(DATA_DIR / "t10k-images-idx3-ubyte.gz", "rb") as fp:
        _ = struct.unpack(">H", fp.read(2))  # dump padding bytes

        (data_type,) = struct.unpack(">c", fp.read(1))
        assert data_type == ALLOWED_TYPES["UNSIGNED_BYTE"]

        number_of_dimensions = ord(struct.unpack(">c", fp.read(1))[0])
        assert number_of_dimensions == 3

        (num_images,) = struct.unpack(">I", fp.read(4))
        assert num_images == 10_000

        (num_rows,) = struct.unpack(">I", fp.read(4))
        (num_cols,) = struct.unpack(">I", fp.read(4))
        assert num_rows == num_cols == 28

        raw = fp.read()
        assert len(raw) == num_images * num_rows * num_cols

    data = np.frombuffer(raw, dtype=np.dtype(np.uint8).newbyteorder(">"))
    data = data.reshape((num_images, num_rows, num_cols))
    return data


def load_train_data():
    with gzip.open(DATA_DIR / "train-images-idx3-ubyte.gz", "rb") as fp:
        _ = struct.unpack(">H", fp.read(2))  # dump padding bytes

        (data_type,) = struct.unpack(">c", fp.read(1))
        assert data_type == ALLOWED_TYPES["UNSIGNED_BYTE"]

        number_of_dimensions = ord(struct.unpack(">c", fp.read(1))[0])
        assert number_of_dimensions == 3

        (num_images,) = struct.unpack(">I", fp.read(4))
        assert num_images == 60_000

        (num_rows,) = struct.unpack(">I", fp.read(4))
        (num_cols,) = struct.unpack(">I", fp.read(4))
        assert num_rows == num_cols == 28

        raw = fp.read()
        assert len(raw) == num_images * num_rows * num_cols

    data = np.frombuffer(raw, dtype=np.dtype(np.uint8).newbyteorder(">"))
    data = data.reshape((num_images, num_rows, num_cols))

    return data


def load_test_labels():
    with gzip.open(DATA_DIR / "t10k-labels-idx1-ubyte.gz", "rb") as fp:
        _ = struct.unpack(">H", fp.read(2))  # dump padding bytes

        (data_type,) = struct.unpack(">c", fp.read(1))
        assert data_type == ALLOWED_TYPES["UNSIGNED_BYTE"]

        number_of_dimensions = ord(struct.unpack(">c", fp.read(1))[0])
        assert number_of_dimensions == 1

        (num_images,) = struct.unpack(">I", fp.read(4))
        assert num_images == 10_000

        raw = fp.read()
        assert len(raw) == num_images

    data = np.frombuffer(raw, dtype=np.dtype(np.uint8).newbyteorder(">"))
    return data


def load_train_labels():
    with gzip.open(DATA_DIR / "train-labels-idx1-ubyte.gz", "rb") as fp:
        _ = struct.unpack(">H", fp.read(2))  # dump padding bytes

        (data_type,) = struct.unpack(">c", fp.read(1))
        assert data_type == ALLOWED_TYPES["UNSIGNED_BYTE"]

        number_of_dimensions = ord(struct.unpack(">c", fp.read(1))[0])
        assert number_of_dimensions == 1

        (num_images,) = struct.unpack(">I", fp.read(4))
        assert num_images == 60_000

        raw = fp.read()
        assert len(raw) == num_images

    data = np.frombuffer(raw, dtype=np.dtype(np.uint8).newbyteorder(">"))
    return data
