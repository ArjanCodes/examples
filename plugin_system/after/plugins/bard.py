"""Game extension that adds a bard character."""

from dataclasses import dataclass

import game.factory


@dataclass
class Bard:

    name: str
    instrument: str = "flute"

    def make_a_noise(self) -> None:
        print(
            f"I am {self.name} and I play the {self.instrument}. Toss a coin to your Witcher!"
        )


def register() -> None:
    game.factory.register("bard", Bard)
