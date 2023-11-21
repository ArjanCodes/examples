from visualizers.plot import visualize_plot
from visualizers.console import visualize_console
from rules import birth_rule, lonely_death_rule, stay_alive_rule, over_populate_rule
from game import Game

ROWS = 20
COLS = 20
RULES = [birth_rule, lonely_death_rule, stay_alive_rule, over_populate_rule]
GENERATIONS = 60
SLEEP_TIME = 0.1
OUTPUT_TYPE = "visualizer"  # console | visualizer


def main() -> None:
    game = Game(ROWS, COLS, RULES)

    game.grid.grid[0][2] = 1
    game.grid.grid[1][3] = 1
    game.grid.grid[2][1] = 1
    game.grid.grid[2][2] = 1
    game.grid.grid[2][3] = 1

    if OUTPUT_TYPE == "visualizer":
        visualize_plot(game, GENERATIONS, SLEEP_TIME)
    elif OUTPUT_TYPE == "console":
        visualize_console(game, GENERATIONS, SLEEP_TIME)


if __name__ == "__main__":
    main()
