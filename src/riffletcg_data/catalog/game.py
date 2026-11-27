"""A game: its mechanics, its cards, and its units."""

from dataclasses import dataclass, field

from riffletcg_data.catalog.card import Card
from riffletcg_data.catalog.component import Component
from riffletcg_data.catalog.mechanic import Mechanic
from riffletcg_data.catalog.unit import Unit


@dataclass
class Game:
    """A game Riffle covers.

    Attributes:
        code: Its short code, such as ``mtg``.
        name: Its full name.
        fields: The names of the game's own fields, for each class that has them.
        mechanics: Its mechanics, by name.
        cards: Its cards, by ID.
        units: Its units, by ID.
    """

    code: str
    name: str
    fields: dict[type, tuple[str, ...]]
    mechanics: dict[str, Mechanic] = field(default_factory=dict)
    cards: dict[str, Card] = field(default_factory=dict)
    units: dict[str, Unit] = field(default_factory=dict)

    def add(self, item: Card | Unit) -> None:
        """Add a card or a unit, failing if anything on it isn't the game's."""
        if isinstance(item, Card):
            parts: tuple[Card | Component, ...] = (item, *item.faces)
            for _ in parts:
                self.cards[item.id] = item
        else:
            self._check(item)
            self.units[item.id] = item

    def _check(self, part: Card | Component) -> None:
        """Fail if a part has a field or a mechanic the game doesn't declare."""
        unknown = part.fields.keys() - set(self.fields.get(type(part), ()))
        if isinstance(part, Component):
            unknown |= set(part.mechanics) - self.mechanics.keys()
        if unknown:
            raise ValueError(f"{part.name}: not in {self.name}: {sorted(unknown)}")
