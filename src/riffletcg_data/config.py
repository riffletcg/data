"""Paths shared across riffletcg-data."""

import os
from pathlib import Path


def folder(override: str, xdg: str, default: str) -> Path:
    """Return one of Riffle's folders, as the environment sets it.

    Args:
        override: The variable that names the folder outright, such as
            ``RIFFLETCG_DATA``.
        xdg: The XDG variable that names the base folder, such as
            ``XDG_DATA_HOME``.
        default: The base folder under home when ``xdg`` is unset, such as
            ``.local/share``.

    Returns:
        The override if it is set, else ``riffletcg/data`` under the base folder.
    """
    base = Path(os.environ.get(xdg) or Path.home() / default)
    return Path(os.environ.get(override) or base / "riffletcg" / "data")


CACHE_DIR = folder("RIFFLETCG_CACHE", "XDG_CACHE_HOME", ".cache")
DATA_DIR = folder("RIFFLETCG_DATA", "XDG_DATA_HOME", ".local/share")
