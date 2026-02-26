from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Iterable

type Action[C] = Callable[[C], None]


class InvalidTransition(Exception):
    pass


@dataclass
class StateMachine[S: Enum, E: Enum, C]:
    transitions: dict[tuple[S, E], tuple[S, Action[C]]] = field(
        default_factory=dict[tuple[S, E], tuple[S, Action[C]]]
    )

    def add_transition(
        self, from_state: S, event: E, to_state: S, func: Action[C]
    ) -> None:
        self.transitions[(from_state, event)] = (to_state, func)

    def next_transition(self, state: S, event: E) -> tuple[S, Action[C]]:
        try:
            return self.transitions[(state, event)]
        except KeyError as e:
            raise InvalidTransition(f"Cannot {event.name} when {state.name}") from e

    def handle(self, ctx: C, state: S, event: E) -> S:
        next_state, action = self.next_transition(state, event)
        action(ctx)
        return next_state

    def transition(self, from_state: S | Iterable[S], event: E, to_state: S):
        if not isinstance(from_state, Iterable):
            from_state = (from_state,)

        def decorator(func: Action[C]) -> Action[C]:
            for s in from_state:
                self.add_transition(s, event, to_state, func)
            return func

        return decorator
