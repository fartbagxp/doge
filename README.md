# Overview

![Last Run](https://github.com/fartbagxp/doge/actions/workflows/deploy.yml/badge.svg)

This repository is intended to backup DOGE savings from [https://doge.gov/savings](https://doge.gov/savings).

It is intended to run nightly and produce a set of [raw data files](data/raw).

## Information Location

The information came from [https://doge.gov/savings](https://doge.gov/savings).

> [!NOTE]
> The API Swagger page can be found in [https://api.doge.gov/docs](https://api.doge.gov/docs).

## How to run

With [uv](https://github.com/astral-sh/uv), run this via `uv run python main.py data/raw/`

## Development

To get started with development, run the following:

```bash
uv venv
source .venv/bin/activate
uv sync --all-extras --dev
```

To add a new dependency, like requests, run this:

```bash
uv add requests
```

To add a new dependency to a group like a lint group to segment dependencies, run this:

```bash
uv add --group lint ruff
```

To run the code from main.py, run it via uv environment.

```bash
uv run main.py data/raw
```

To exit out of the virtual environment (venv), run the following:

```bash
deactivate
```

To figure out which dependency may be outdated, find the dependencies via:

```bash
uv pip list --outdated
```

To create a new dependency lock file manually (optional as it should happen automatically on uv add):

```bash
uv lock
```

To upgrade dependencies, run:

```bash
uv lock --upgrade
```
