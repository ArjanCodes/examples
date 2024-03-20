from collections import defaultdict
from typing import Dict


class Scoreboard:
    """Scoreboard class to register player, track points and display the card"""

    def __init__(self) -> None:
        self.points: Dict[str, int] = defaultdict(int)

    def register_player(self, user_name: str):
        self.points[user_name] = 0

    def display_scores(self):
        print("Scoreboard:")
        print("======================================")
        for user, score in self.points.items():
            print(f"{user} : {score}", end="\t")
        print("\n======================================")
