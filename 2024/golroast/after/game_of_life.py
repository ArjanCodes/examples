from visualizers.plot import visualize_plot
from visualizers.console import visualize_console
from rules import BirthRule, LonelyDeathRule, StayAliveRule, OverPopulateRule


class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[0] * self.cols for _ in range(self.rows)]

    def is_cell_in_bounds(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def is_alive(self, row, col):
        return self.grid[row][col] == 1 if self.is_cell_in_bounds(row, col) else 0

    def alive_neighbors(self, row, col):
        offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        return sum(
            [self.is_alive(row + off_y, col + off_x) for off_y, off_x in offsets]
        )

    def __str__(self):
        rows = ["  ".join(map(str, row)) for row in self.grid]
        return "\n".join(rows)


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


def main():
    config = {
        "rows": 20,
        "cols": 20,
        "generations": 120,
        "rules": [BirthRule, StayAliveRule, LonelyDeathRule, OverPopulateRule],
        "sleep_time": 0.1,
        "output_type": "visualizer",  # console | visualizer
    }

    game = Game(config["rows"], config["cols"], config["rules"])

    game.grid.grid[0][2] = 1
    game.grid.grid[1][3] = 1
    game.grid.grid[2][1] = 1
    game.grid.grid[2][2] = 1
    game.grid.grid[2][3] = 1

    if config["output_type"] == "visualizer":
        visualize_plot(game, config["generations"], config["sleep_time"])
    elif config["output_type"] == "console":
        visualize_console(game, config["generations"], config["sleep_time"])


if __name__ == "__main__":
    main()
