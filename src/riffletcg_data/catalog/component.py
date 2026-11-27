"""Anything with rules on it."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Component:
    """Anything with rules on it: a card's face, or a unit.

    Attributes:
        name: Its name.
        mechanics: The names of the mechanics it has.
        fields: Its game's own fields, such as a Magic face's mana_cost.
    """

    name: str
    mechanics: tuple[str, ...]
    fields: dict[str, Any]
