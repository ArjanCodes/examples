import time
from typing import Protocol


class Game(Protocol):
    def update(self): ...

    @property
    def raw_grid(self) -> list[list[int]]: ...


def visualize_console(game: Game, generations: int, sleep_time: float):
    for generation in range(1, generations):
        game.update()
        print(f"Generation {generation}:\n")
        print(game)
        time.sleep(sleep_time)
