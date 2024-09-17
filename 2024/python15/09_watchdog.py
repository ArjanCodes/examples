import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f"{event.src_path} has been modified")


def main():
    # Set up the observer and file system handler
    path_to_watch = "."
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=True)

    # Start observing
    observer.start()
    print(f"Monitoring changes in {path_to_watch}... Press Ctrl+C to stop.")

    try:
        # Keep the script running indefinitely
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Stop the observer when the script is interrupted
        observer.stop()

    observer.join()


if __name__ == "__main__":
    main()
