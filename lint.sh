#!/usr/bin/env bash

set -eu

command -v csvlint >/dev/null 2>&1 || { echo "csvlint is not installed." >&2; exit 1; }

dir=${1:-.}

find "$dir" -type f -name "*.csv" | while read -r file; do
  echo "checking on file: $file"
  csvlint "$file"
done
