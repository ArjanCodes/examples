from visualizers.plot import visualize_plot
from visualizers.console import visualize_console
from rules import BirthRule, LonelyDeathRule, StayAliveRule, OverPopulateRule
from game import Game


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
