import sys

from PyQt6 import QtWidgets

from viewmodel import TodoList


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    viewmodel = TodoList()
    viewmodel.show()
    app.exec()


if __name__ == "__main__":
    main()
