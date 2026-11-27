"""A card, made up of its faces."""

from dataclasses import dataclass
from typing import Any

from riffletcg_data.catalog.face import Face


@dataclass(frozen=True)
class Card:
    """A card in any game.

    Attributes:
        id: Its ID at its source, such as Scryfall's oracle_id.
        name: Its full name, such as "Wear // Tear".
        faces: Its faces, main face first. An ordinary card has one.
        fields: Its game's own fields for the card as a whole, such as layout.
    """

    id: str
    name: str
    faces: tuple[Face, ...]
    fields: dict[str, Any]

    @property
    def mechanics(self) -> tuple[str, ...]:
        """Every mechanic on any of the card's faces, without repeats."""
        return tuple(dict.fromkeys(m for face in self.faces for m in face.mechanics))
