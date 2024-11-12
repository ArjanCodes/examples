from commands.show_files import show_files
from dictionary import DataDictionary
from events import clear_events, register_event
from pandas import DataFrame


def test_show_files(capsys):
    register_event("*", print)
    # create a mock model
    model = DataDictionary()
    model.create("test", DataFrame())
    model.create("test2", DataFrame())

    # now check that show_files prints the correct message
    show_files(model)
    out, err = capsys.readouterr()

    # this should print:
    # Files presently stored:
    # Alias: test
    # Alias: test2
    assert out == "Files presently stored:\nAlias: test\nAlias: test2\n"
    clear_events()
