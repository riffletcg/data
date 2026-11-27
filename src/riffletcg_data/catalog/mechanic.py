"""A named rule a game's components can have."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Mechanic:
    """A named rule, such as Scry in Magic or Go again in Flesh and Blood.

    Attributes:
        name: Its name as printed.
        kind: What sort of mechanic it is, in the game's own terms, such as
            "keyword action".
    """

    name: str
    kind: str
