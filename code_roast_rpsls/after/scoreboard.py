class Scoreboard:
    """Scoreboard class to register player, track points and display the card"""

    def __init__(self) -> None:
        self.points: dict[str, int] = {}

    def register_player(self, user_name: str):
        self.points[user_name] = 0

    def win_round(self, player_name: str):
        self.points[player_name] += 1
