import random

from entity import Entity


def _entities_str() -> str:
    return ", ".join(
        f"({index + 1} for {entity})" for index, entity in enumerate(Entity)
    )


class CLI:
    def pick_player_entity(self) -> Entity:
        while True:
            try:
                print(f"Select {_entities_str()}:", end="\t")
                choice = int(input())

                if 0 < choice < len(Entity) + 1:
                    return list(Entity)[choice - 1]
                print("Please select from available choices")
            except ValueError:
                print("You entered something other than a number")

    def pick_cpu_entity(self) -> Entity:
        return random.choice(list(Entity))

    def read_player_name(self) -> str:
        print("Please enter your name:", end="\t")
        return input().strip()

    def display_rules(self) -> None:
        print("Rock paper scissor spock and lizard...\n Welcome to the game.")
        print("Rules are simple...")
        print(
            "Scissors decapitate Lizard, Scissors cuts paper, paper covers rock, rock crushes lizard, lizard poisons Spock, Spock smashes scissors, scissors decapitates lizard, lizard eats paper, paper disproves Spock, Spock vaporizes rock, and as it always has, rock crushes scissors."
        )
        print("To begin press [Enter]")
        _ = input()

    def display_current_round(
        self, user: str, cpu: str, user_entity: Entity, cpu_entity: Entity
    ) -> None:
        print(f"{user} ({user_entity}) x {cpu} ({cpu_entity})")
        print("....")

    def display_tie(self) -> None:
        print("It's a tie..")

    def display_round_winner(
        self, winner_name: str, winner_entity: Entity, message: str
    ) -> None:
        print(f"{winner_name} ({winner_entity}) wins the round as {message}")

    def display_scores(self, scores: dict[str, int]) -> None:
        print("Scoreboard:")
        print("======================================")
        for user, score in scores.items():
            print(f"{user} : {score}", end="\t")
        print("\n======================================")
