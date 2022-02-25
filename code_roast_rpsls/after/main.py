from cli import CLI
from game import Game
from scoreboard import Scoreboard


def main() -> None:
    interface = CLI()
    user_name = interface.read_player_name()
    game = Game(Scoreboard(), interface, user_name)
    game.play()


if __name__ == "__main__":
    main()
