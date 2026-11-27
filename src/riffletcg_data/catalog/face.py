"""One face of a card."""

from dataclasses import dataclass

from riffletcg_data.catalog.component import Component


@dataclass(frozen=True)
class Face(Component):
    """One face of a card: a side, a half, or the whole of an ordinary card.

    Attributes:
        type_line: Its types as printed, such as "Creature — Giant".
        text: Its rules text.
    """

    type_line: str | None
    text: str | None
