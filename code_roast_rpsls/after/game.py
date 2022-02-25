from dataclasses import dataclass

from rules import get_winner
from scoreboard import Scoreboard
from ui import UI


@dataclass
class Game:
    scoreboard: Scoreboard
    interface: UI
    player_name: str
    cpu_name: str = "cpu"

    def turn(self) -> None:
        player_entity = self.interface.pick_player_entity()
        cpu_entity = self.interface.pick_cpu_entity()

        self.interface.display_current_round(
            self.player_name, self.cpu_name, player_entity, cpu_entity
        )

        # REVIEWERS: I feel like the code below can be rewritten to be shorter/clearer, but have not figured out the best way
        # to do it. The code for handling the player vs the cpu as the winner is almost the same. I'm open to suggestions.
        winner, message = get_winner(player_entity, cpu_entity)
        if not winner:
            self.interface.display_tie()
        elif winner == player_entity:
            self.interface.display_round_winner(self.player_name, winner, message)
            self.scoreboard.win_round(self.player_name)
        else:
            self.interface.display_round_winner(self.cpu_name, winner, message)
            self.scoreboard.win_round(self.cpu_name)

    def play(self, max_round: int = 5):
        # register players in scoreboard
        self.scoreboard.register_player(self.player_name)
        self.scoreboard.register_player(self.cpu_name)

        # display the rules
        self.interface.display_rules()

        # play the game
        for _ in range(max_round):
            self.turn()
            # REVIEWERS: I've changed this so that the score board no longer prints itself, but the UI is
            # responsible for that. Does this violate the Law of Demeter? Or do you think this is acceptable?
            # Let me know.
            self.interface.display_scores(self.scoreboard.points)
