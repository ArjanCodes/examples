import os
from contextlib import contextmanager


@contextmanager
def change_dir(destination: str):
    """Sets a destination for exported files."""
    cwd = os.getcwd()
    try:
        __dest = os.path.realpath(destination)
        if not os.path.exists(__dest):
            os.mkdir(__dest)
        os.chdir(__dest)
        yield
    finally:
        os.chdir(cwd)
