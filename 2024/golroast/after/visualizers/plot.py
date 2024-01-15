from typing import Protocol
import matplotlib.pyplot as plt


class Game(Protocol):
    def update(self):
        ...

    @property
    def raw_grid(self) -> list[list[int]]:
        ...


def visualize_plot(game: Game, generations: int, sleep_time: float):
    _, ax = plt.subplots()
    game_display = ax.imshow(game.raw_grid, cmap="gray_r")

    ax.set_xticks([])
    ax.set_yticks([])

    for _ in range(generations):
        game.update()
        game_display.set_data(game.raw_grid)
        plt.draw()
        plt.pause(sleep_time)

    plt.show()
