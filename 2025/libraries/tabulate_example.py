from tabulate import tabulate

table = [["Alice", 24], ["Bob", 19]]
print(tabulate(table, headers=["Name", "Age"]))
