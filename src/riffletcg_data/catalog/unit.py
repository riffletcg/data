"""A unit in a wargame."""

from dataclasses import dataclass

from riffletcg_data.catalog.component import Component


@dataclass(frozen=True)
class Unit(Component):
    """A unit in a wargame.

    Attributes:
        id: Its ID at its source.
        faction: The faction it belongs to.
    """

    id: str
    faction: str
