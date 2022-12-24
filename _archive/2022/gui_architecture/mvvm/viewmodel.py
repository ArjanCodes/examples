UI_FILE = "view.ui"

from PyQt6 import QtGui, QtWidgets, uic
from PyQt6.QtCore import QModelIndex

from model import create_model


class TodoList(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        QtWidgets.QMainWindow.__init__(self)
        uic.loadUi(UI_FILE, self)
        self.task_list_model = create_model()
        self.task_list.setModel(self.task_list_model)
        self.task_list.selectionModel().selectionChanged.connect(
            self.on_change_selection
        )
        self.todo_edit.returnPressed.connect(self.on_add_task)
        self.delete_button.pressed.connect(self.on_delete_task)
        # self.delete_button.setEnabled(False)

    def on_add_task(self) -> None:
        text: str = self.todo_edit.text()
        if not text:
            return
        self.task_list_model.appendRow(QtGui.QStandardItem(text))
        self.todo_edit.clear()

    def on_delete_task(self) -> None:
        indexes: list[QModelIndex] = self.task_list.selectedIndexes()
        if not indexes:
            return
        self.task_list_model.removeRow(indexes[0].row())
        self.task_list.clearSelection()

    def on_change_selection(self) -> None:
        indexes: list[QModelIndex] = self.task_list.selectedIndexes()
        self.delete_button.setEnabled(bool(indexes))
