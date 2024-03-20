from typing import Callable
from grid import Grid

type Rule = Callable[[int, int], int | None]


class Game:
    def __init__(self, grid: Grid, rules: list[Rule] | None = None):
        self.grid = grid
        self.rules = rules if rules else []

    def set_grid_cell(self, row: int, col: int, value: int) -> None:
        self.grid.set_cell(row, col, value)

    @property
    def raw_grid(self) -> list[list[int]]:
        return self.grid.raw

    def update(self):
        new_grid = Grid(self.grid.rows, self.grid.cols)
        for row, col, cell in self.grid:
            alive_neighbors = self.grid.alive_neighbors(row, col)
            new_cell = self._apply_rules_to_cell(cell, alive_neighbors)
            new_grid.set_cell(row, col, new_cell)

        self.grid = new_grid

    def _apply_rules_to_cell(self, cell: int, alive_neighbors: int) -> int:
        for rule in self.rules:
            result = rule(cell, alive_neighbors)
            if result is not None:
                return result

        return cell

    def __str__(self):
        return str(self.grid)
