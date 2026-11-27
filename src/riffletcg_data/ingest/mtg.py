"""Build Magic's cards from Scryfall's data."""

from collections.abc import Iterator
from pprint import pprint
from typing import Any

from riffletcg_data.catalog.card import Card
from riffletcg_data.catalog.face import Face
from riffletcg_data.games import MTG
from riffletcg_data.sources import scryfall


def card(entry: dict[str, Any]) -> Card:
    """Build a card and its faces from one Scryfall card object."""
    faces = tuple(
        Face(
            name=part["name"],
            mechanics=(),
            fields={key: part.get(key, entry.get(key)) for key in MTG.fields[Face]},
            type_line=part.get("type_line"),
            text=part.get("oracle_text"),
        )
        for part in entry.get("card_faces") or [entry]
    )
    fields = {key: entry.get(key) for key in MTG.fields[Card]}
    return Card(entry["oracle_id"], entry["name"], faces, fields)


def cards() -> Iterator[Card]:
    """Yield each Magic card the first time it appears in All Cards."""
    seen = set()
    for entry in scryfall.bulk("all_cards"):
        oracle_id = entry.get("oracle_id")
        if oracle_id is None or oracle_id in seen:
            continue
        seen.add(oracle_id)
        yield card(entry)


if __name__ == "__main__":
    # Print the first card of each layout, until five layouts have been seen
    layouts = set()
    for found in cards():
        layout = found.fields["layout"]
        if layout not in layouts:
            layouts.add(layout)
            pprint(found)
            MTG.add(found)
        if len(layouts) == 5:
            break
    print(len(MTG.cards), "cards added to", MTG.name)
