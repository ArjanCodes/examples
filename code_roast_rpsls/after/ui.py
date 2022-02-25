from typing import Protocol

from entity import Entity


class UI(Protocol):
    def pick_player_entity(self) -> Entity:
        """Takes user inputs and selects the entities

        Returns:
            Entity: Entity selected by user
        """
        raise NotImplementedError()

    def pick_cpu_entity(self) -> Entity:
        """Selects a random entity

        Returns:
            Entity: A random entity
        """
        raise NotImplementedError()

    def read_player_name(self) -> str:
        raise NotImplementedError()

    def display_rules(self) -> None:
        raise NotImplementedError()

    def display_current_round(
        self, user: str, cpu: str, user_entity: Entity, cpu_entity: Entity
    ) -> None:
        """Displays current round

        Args:
            user_entity (Entity): Entity selected by user
            cpu_entity (Entity): Entity selected by cpu
        """
        raise NotImplementedError()

    def display_tie(self) -> None:
        raise NotImplementedError()

    def display_round_winner(
        self, winner_name: str, winner_entity: Entity, message: str
    ) -> None:
        raise NotImplementedError()

    def display_scores(self, scores: dict[str, int]) -> None:
        raise NotImplementedError()
