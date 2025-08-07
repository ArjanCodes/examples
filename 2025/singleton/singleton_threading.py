from threading import Thread

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            print(f"Creating instance of {cls.__name__}")
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
    
class Unsafe(metaclass=Singleton):
    def __init__(self):
        print("Initializing...")

def main() -> None:
    threads = [Thread(target=Unsafe) for _ in range(20)]
    [t.start() for t in threads]
    [t.join() for t in threads]

if __name__ == "__main__":
    main()