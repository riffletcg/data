"""Every game Riffle covers, and the fields its cards and faces have."""

from riffletcg_data.catalog.card import Card
from riffletcg_data.catalog.face import Face
from riffletcg_data.catalog.game import Game

MTG = Game(
    "mtg",
    "Magic: The Gathering",
    fields={
        Card: ("layout", "cmc", "color_identity", "legalities"),
        Face: (
            "mana_cost",
            "colors",
            "color_indicator",
            "power",
            "toughness",
            "loyalty",
        ),
    },
)

GAMES = {game.code: game for game in (MTG,)}
