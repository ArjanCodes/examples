from src.model.dictionary import DataDictionary
from src.view.shell_view import Shell
from src.controller.shell_controller import ShellController

import pandas as pd




if __name__ == "__main__":
    model = DataDictionary()

    model.create('file1', pd.read_csv('file1.csv'))
    model.create('file2', pd.read_csv('file2.csv'))


    view = Shell(model)

    controller = ShellController(model, view)
