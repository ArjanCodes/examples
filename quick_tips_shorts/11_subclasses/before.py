from dataclasses import dataclass


@dataclass
class Enemy:
    strength: int
    dexterity: int
    intelligence: int
    health: int


class Zombie(Enemy):
    def __init__(self):
        super().__init__(strength=30, dexterity=10, intelligence=1, health=100)


class EvilOverlord(Enemy):
    def __init__(self):
        super().__init__(strength=10, dexterity=10, intelligence=10, health=100)


def main() -> None:
    zombie = Zombie()
    print(zombie)
    arjan = EvilOverlord()
    print(arjan)


if __name__ == "__main__":
    main()
