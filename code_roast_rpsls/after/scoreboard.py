from ui import UI


class Scoreboard:
    def __init__(self) -> None:
        self.points: dict[str, int] = {}

    def register_player(self, user_name: str) -> None:
        self.points[user_name] = 0

    def win_round(self, player_name: str) -> None:
        self.points[player_name] += 1

    def to_display(self, ui: UI) -> None:
        ui.display_scores(self.points)
