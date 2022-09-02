from dataclasses import dataclass


@dataclass
class Enemy:
    strength: int
    dexterity: int
    intelligence: int
    health: int


def create_zombie() -> Enemy:
    return Enemy(strength=30, dexterity=10, intelligence=1, health=100)


def create_evil_overlord() -> Enemy:
    return Enemy(strength=10, dexterity=10, intelligence=10, health=100)


def main() -> None:
    zombie = create_zombie()
    print(zombie)
    arjan = create_evil_overlord()
    print(arjan)


if __name__ == "__main__":
    main()
