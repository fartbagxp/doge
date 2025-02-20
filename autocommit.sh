#!/usr/bin/env bash

set -eu

if [[ -n $(git status --porcelain) ]]; then
  echo "Changes detected. Committing to main."
  git add .
  git commit -m "Auto-commit sync on: $(date '+%Y-%m-%d %H:%M:%S')"
  git push origin main
else
  echo "No changes detected. Exiting."
fi
