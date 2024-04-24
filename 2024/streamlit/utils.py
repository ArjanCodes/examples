import random
from dataclasses import astuple, dataclass

from py_wanderer import ALGORITHMS, HEURISTICS, Heuristic, Maze, PathfindingAlgorithm

SolvingStrategy = tuple[PathfindingAlgorithm, Heuristic]
SolvingStrategies = tuple[SolvingStrategy]


@dataclass
class MazeConfig:
    seed: int
    width: int
    height: int
    num_rooms: int
    room_size_range: tuple[int, int]
    solving_strategies: SolvingStrategies = ((ALGORITHMS[0], HEURISTICS[0]),)

    def __hash__(self):
        return hash(astuple(self))


def generate_maze(
    seed: int, width: int, height: int, num_rooms: int, room_size_range: tuple[int, int]
):
    width += width % 2 == 0
    height += height % 2 == 0
    start, end = (1, 1), (height - 2, width - 2)
    state = random.getstate()
    random.seed(seed)
    maze = Maze(width, height, start, end, num_rooms, room_size_range).generate()
    random.setstate(state)
    return maze


def solve_maze(maze: Maze, strategies: SolvingStrategies):
    return maze.solve_many(list(strategies))
