from PyQt6 import QtGui

TASK_LIST = [
    "Process email inbox",
    "Write blog post",
    "Prepare video scripts",
    "Tax accounting",
    "Prepare presentation",
    "Go to the gym",
]


def create_model() -> QtGui.QStandardItemModel:
    model = QtGui.QStandardItemModel()
    for task in TASK_LIST:
        item = QtGui.QStandardItem(task)
        model.appendRow(item)
    return model
