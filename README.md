# Overview

![Last Run](https://github.com/fartbagxp/doge/actions/workflows/deploy.yml/badge.svg)

This repository is intended to backup DOGE savings from [https://doge.gov/savings](https://doge.gov/savings).

It is intended to run nightly and produce a set of [raw data files](data/raw).

## Information Location

The information came from [https://doge.gov/savings](https://doge.gov/savings).

> [!NOTE]
> The API Swagger page can be found in [https://api.doge.gov/docs](https://api.doge.gov/docs).

## How to run

With [uv](https://github.com/astral-sh/uv), run it locally:

```bash
uv run python main.py data/raw/
```
