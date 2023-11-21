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
