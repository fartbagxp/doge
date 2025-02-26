# Overview

![Last Run](https://github.com/fartbagxp/doge/actions/workflows/main.yml/badge.svg)

This repository is intended to backup DOGE savings from [https://doge.gov/savings](https://doge.gov/savings)

It is intended to run nightly.

## Information Location

The information came from [https://doge.gov/savings](https://doge.gov/savings).

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
