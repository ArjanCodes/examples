from controller import Controller
from model import Model
from view import TodoList


def main() -> None:
    model = Model()
    view = TodoList(model)
    controller = Controller(model, view)
    controller.run()


if __name__ == "__main__":
    main()
