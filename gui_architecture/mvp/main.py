from model import Model
from presenter import Presenter
from view import TodoList


def main() -> None:
    model = Model()
    view = TodoList()
    presenter = Presenter(model, view)
    presenter.run()


if __name__ == "__main__":
    main()
