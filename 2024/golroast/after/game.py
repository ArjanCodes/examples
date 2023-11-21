from grid import Grid


class Game:
    def __init__(self, rows, cols, rules=None):
        self.grid = Grid(rows, cols)
        self.rules = rules if rules else []

    def update(self):
        new_grid = [[0 for _ in range(self.grid.cols)] for _ in range(self.grid.rows)]
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                cell = self.grid.grid[row][col]
                alive_neighbors = self.grid.alive_neighbors(row, col)

                new_cell = None
                for rule in self.rules:
                    result = rule.apply(cell, alive_neighbors)
                    if result is not None:
                        new_cell = result
                        break

                new_grid[row][col] = new_cell if new_cell is not None else cell

        self.grid.grid = new_grid
