# type: ignore
# source: https://medium.com/@rodney_ragan/writing-a-spinner-a-spinning-progression-indicator-in-python-6f82e3a3bee
import functools
import sys
import threading
from datetime import timedelta
from itertools import cycle
from time import sleep, time

from src.tracing.logger import logger


def spin(msg: str, start: float, frames, stop_spin: threading.Event):
    while not stop_spin.is_set():
        frame = next(frames)
        sec, fsec = divmod(round(100 * (time() - start)), 100)
        frame += " ({} : {}.{:02.0f})".format(msg, timedelta(seconds=sec), fsec)
        print("\r", frame, sep="", end="", flush=True)
        sleep(0.1)


def spinner(msg: str = "Elapsed Time"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper_decrorator(*args, **kwargs):
            stop_spin = threading.Event()
            start = time()
            spin_thread = threading.Thread(
                target=spin,
                args=(
                    msg,
                    start,
                    cycle(
                        [
                            " [    ]:",
                            " [=   ]:",
                            " [==  ]:",
                            " [=== ]:",
                            " [ ===]:",
                            " [  ==]:",
                            " [   =]:",
                        ]
                    ),
                    stop_spin,
                ),
            )
            spin_thread.start()

            try:
                value = func(*args, **kwargs)
            except Exception as e:
                logger.error(e)
                sys.exit(1)
            finally:
                stop = time()
                if spin_thread:
                    stop_spin.set()
                    spin_thread.join()
                print("\n", flush=True)
                print("=" * 60)
                print("Elapsed Time: ")
                print("=" * 60)
                print(stop - start)
                print("=" * 60)
                print()
            return value

        return wrapper_decrorator

    return decorator
