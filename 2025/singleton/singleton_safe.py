# singleton.py
from __future__ import annotations

import threading
from typing import Any


class Singleton(type):
    _instances: dict[type, Any] = {}
    _locks: dict[type, threading.Lock] = {}
    _global_lock = threading.Lock()  # protects _locks map creation

    def __call__(cls, *args, **kwargs):
        # Fast path: already created
        if cls in cls._instances:
            return cls._instances[cls]

        # Ensure a per-class lock exists
        with cls._global_lock:
            lock = cls._locks.setdefault(cls, threading.Lock())

        # Double-checked locking: only one thread creates the instance
        with lock:
            if cls not in cls._instances:
                print(f"Creating instance of {cls.__name__}")
                instance = super().__call__(*args, **kwargs)  # calls __init__ once
                cls._instances[cls] = instance

        return cls._instances[cls]
