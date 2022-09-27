from gui import SmartApp
from speaker import Speaker


def main() -> None:
    speaker_facade = Speaker()
    app = SmartApp(speaker_facade.send_message)
    app.mainloop()


if __name__ == "__main__":
    main()
