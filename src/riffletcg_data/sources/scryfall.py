"""Scryfall's bulk files."""

import json
import shutil
import time
import urllib.request
from collections.abc import Collection
from http.client import HTTPException
from pathlib import Path
from typing import Any

from riffletcg_data.config import CACHE_DIR

HEADERS = {"User-Agent": "riffletcg-data/0.1", "Accept": "*/*"}
API = "https://api.scryfall.com"
SCRYFALL_DIR = CACHE_DIR / "scryfall"
ATTEMPTS = 3


def get(url: str) -> Any:
    """Open a URL with the headers Scryfall requires.

    Args:
        url: The address to request.

    Returns:
        The open response, to use in a ``with`` block.
    """
    return urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS))


def save(url: str, path: Path, size: int) -> None:
    """Download a URL to a path, failing unless it arrives at the expected size.

    The download goes to a ``.part`` file beside the path and is renamed once it
    is whole, so a file under its real name is always complete.

    Args:
        url: The address to download.
        path: Where the finished file goes.
        size: The file's expected size in bytes.

    Raises:
        OSError: If the file arrives at any other size.
    """
    part = path.with_name(f"{path.name}.part")
    with get(url) as response, part.open("wb") as bulk:
        shutil.copyfileobj(response, bulk)
    if part.stat().st_size != size:
        raise OSError(f"{path.name}: the download is incomplete")
    part.rename(path)


def fetch(url: str, path: Path, size: int) -> None:
    """Save a URL to a path, trying again after a failure, up to ATTEMPTS times.

    Each wait is twice the last: 2 seconds after the first failure, then 4.

    Args:
        url: The address to download.
        path: Where the finished file goes.
        size: The file's expected size in bytes.

    Raises:
        OSError: If the last try can't connect, write, or get the whole file.
        HTTPException: If the last try's response breaks off.
    """
    for attempt in range(1, ATTEMPTS + 1):
        try:
            return save(url, path, size)
        except OSError, HTTPException:
            if attempt == ATTEMPTS:
                raise
            time.sleep(2**attempt)


def download() -> list[Path]:
    """Bring the cache up to date with Scryfall's bulk files.

    Downloads each file the cache lacks, then deletes every other file there.

    Returns:
        The path of each current bulk file, in the order Scryfall lists them.
    """
    with get(f"{API}/bulk-data") as response:
        files = json.load(response)["data"]
    SCRYFALL_DIR.mkdir(parents=True, exist_ok=True)
    current = []
    for file in files:
        url = file["jsonl_download_uri"]
        path = SCRYFALL_DIR / Path(url).name
        if not path.exists():
            fetch(url, path, file["compressed_size"])
        current.append(path)
    prune(current)
    return current


def prune(keep: Collection[Path]) -> None:
    """Delete every file in the Scryfall cache that isn't in keep.

    Args:
        keep: The paths to leave in place.
    """
    for path in SCRYFALL_DIR.iterdir():
        if path not in keep:
            path.unlink()


if __name__ == "__main__":
    for path in download():
        print(path)
