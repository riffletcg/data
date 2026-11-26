"""Entry point for riffletcg-data."""

import logging
import os

from riffletcg_data.config import DATA_DIR

log = logging.getLogger(__name__)


def setup_logging() -> None:
    """Configure root logging; set LOG_LEVEL=INFO or DEBUG for more output."""
    logging.basicConfig(
        level=os.environ.get("LOG_LEVEL", "WARNING").upper(),
        format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def main() -> int:
    """Run riffletcg-data.

    Returns:
        Process exit code (0 on success).
    """
    setup_logging()
    log.info("data dir: %s", DATA_DIR)

    print("Hello from riffletcg-data!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
