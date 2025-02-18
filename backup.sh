#!/usr/bin/env bash

[[ -v VERBOSE ]] && set -x
set -eu

target="${1}/data/raw"

echo "doge savings - contracts and leases"
curl --retry 5 --max-time 180 -f https://www.doge.gov/api/receipts/overview \
  --compressed \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0' \
  -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' \
  -H 'Accept-Language: en-US,en;q=0.5' \
  -H 'Accept-Encoding: gzip, deflate' | jq '.' > "${target}/doge_savings.json"

jq .contracts "${target}/doge_savings.json" > "${target}/doge_contracts_termination.json"
jq .leases "${target}/doge_savings.json" > "${target}/doge_leases_termination.json"

jq -r '(map(keys) | add | unique) as $cols | map(. as $row | $cols | map($row[.])) as $rows | $cols, $rows[] | @csv' "${target}/doge_contracts_termination.json" > "${target}/doge_contracts_termination.csv"
jq -r '(map(keys) | add | unique) as $cols | map(. as $row | $cols | map($row[.])) as $rows | $cols, $rows[] | @csv' "${target}/doge_leases_termination.json" > "${target}/doge_leases_termination.csv"