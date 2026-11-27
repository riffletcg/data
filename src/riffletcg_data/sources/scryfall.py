"""Scryfall's bulk files."""

import gzip
import json
import urllib.request
from collections.abc import Iterator
from typing import Any

HEADERS = {"User-Agent": "riffletcg-data/0.1", "Accept": "*/*"}
API = "https://api.scryfall.com"


def get(url: str) -> Any:
    """Open a URL with the headers Scryfall requires."""
    return urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS))


def bulk(kind: str) -> Iterator[dict[str, Any]]:
    """Yield each object in one of Scryfall's bulk files, such as all_cards."""
    with get(f"{API}/bulk-data/{kind}") as response:
        url = json.load(response)["jsonl_download_uri"]
    with get(url) as response, gzip.open(response, "rt", encoding="utf-8") as file:
        for line in file:
            yield json.loads(line)
