class Grid:
    def __init__(self, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols
        self.grid = [[0] * self.cols for _ in range(self.rows)]

    def is_cell_in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.rows and 0 <= col < self.cols

    def is_alive(self, row: int, col: int) -> bool:
        return self.grid[row][col] == 1 if self.is_cell_in_bounds(row, col) else False

    def alive_neighbors(self, row: int, col: int) -> int:
        offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        return [
            self.is_alive(row + off_y, col + off_x) for off_y, off_x in offsets
        ].count(True)

    def __str__(self):
        rows = ["  ".join(map(str, row)) for row in self.grid]
        return "\n".join(rows)
