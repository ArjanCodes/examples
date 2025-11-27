import json
from functools import wraps
from typing import Any, Callable

# ------------------------------------------------------------
# Generic Types
# ------------------------------------------------------------

type RuleFn[T] = Callable[[T], bool]
type RuleFactory[T] = Callable[..., RuleFn[T]]
type PredicateFactory[T] = Callable[..., Predicate[T]]


# ------------------------------------------------------------
# Global Rule Registry
# ------------------------------------------------------------

RULES: dict[str, PredicateFactory[Any]] = {}


# ------------------------------------------------------------
# Predicate
# ------------------------------------------------------------


class Predicate[T]:
    """
    A composable predicate that supports &, |, and ~ operators.
    Wraps a function (T -> bool).
    """

    def __init__(self, fn: RuleFn[T]):
        self.fn = fn

    def __call__(self, obj: T) -> bool:
        return self.fn(obj)

    def __and__(self, other: Predicate[T]) -> Predicate[T]:
        return Predicate(lambda x: self(x) and other(x))

    def __or__(self, other: Predicate[T]) -> Predicate[T]:
        return Predicate(lambda x: self(x) or other(x))

    def __invert__(self) -> Predicate[T]:
        return Predicate(lambda x: not self(x))


# ------------------------------------------------------------
# Decorators
# ------------------------------------------------------------


def predicate[T](fn: RuleFn[T]) -> Predicate[T]:
    """
    Wrap a simple function(obj) -> bool into a Predicate[T].
    This is used *inside* rule factories when building actual predicates.
    """

    @wraps(fn)
    def wrapper(obj: T) -> bool:
        return fn(obj)

    return Predicate(wrapper)


def rule[T](fn: RuleFactory[T]) -> PredicateFactory[T]:
    """
    Decorator for rule factories.
    """

    @wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Predicate[T]:
        result = fn(*args, **kwargs)
        return Predicate(result)

    RULES[fn.__name__] = wrapper
    return wrapper


# ------------------------------------------------------------
# Config Loader
# ------------------------------------------------------------


def load_rule_from_config(path: str) -> Predicate[Any]:
    """
    Load a rule from a JSON config file that looks like:

    {
      "logic": "AND",
      "conditions": [
        {"name": "is_active", "args": []},
        {"name": "older_than", "args": [30]}
      ]
    }

    The returned object is a composed Predicate[Any].
    """

    with open(path) as f:
        config = json.load(f)

    preds: list[Predicate[Any]] = []

    for cond in config["conditions"]:
        name = cond["name"]
        args = cond.get("args", [])

        if name not in RULES:
            raise ValueError(f"Unknown rule: {name}")

        factory = RULES[name]
        predicate_obj = factory(*args)
        preds.append(predicate_obj)

    combined = preds[0]
    logic = config["logic"]

    for p in preds[1:]:
        combined = (combined & p) if logic == "AND" else (combined | p)

    return combined
