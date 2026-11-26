# riffletcg-data

TODO: one-line description.

## Install

```bash
uv sync                      # creates .venv, installs the package + dev tools
source .venv/bin/activate    # or prefix commands with `uv run`
```

## Usage

```bash
riffletcg-data                        # or: python -m riffletcg_data  (LOG_LEVEL=DEBUG for more output)
```

## Development

```bash
uv run pytest --cov          # tests + coverage
uv run ruff check --fix      # lint
uv run ruff format           # format
uv run mypy                  # type-check
uv add <package>             # add a runtime dependency
uv add --dev <package>       # add a dev dependency
uv run pre-commit autoupdate # bump pinned hook versions
```

## Layout

```
src/riffletcg_data/    package code (main.py = CLI, config.py = paths/settings)
tests/       pytest tests
docs/        notes, design docs, reference PDFs
data/        local data (contents git-ignored)
```
