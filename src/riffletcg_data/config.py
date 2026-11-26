"""Paths and settings shared across riffletcg-data.

PROJECT_ROOT assumes an editable install from the repo (what `uv sync` does).
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "out"
