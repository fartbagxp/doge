#!/usr/bin/env bash

[[ -v VERBOSE ]] && set -x
set -eu

if command -v curl > /dev/null 2>&1 ; then
  echo "curl is installed."
else
  echo "curl not found! Please install curl and run again!"
  exit 1
fi

if command -v jq > /dev/null 2>&1 ; then
  echo "jq is installed."
else
  echo "jq not found! Please install jq and run again!"
  exit 1
fi

# Ensure an input path argument is provided
if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <input_path>"
  exit 1
fi

input_path="$1"
target="${input_path}/data/raw"

echo "doge savings - contracts and leases"

# Perform the curl request ONCE and store response + HTTP status
response=$(curl --retry 5 --max-time 180 -s -w "\n%{http_code}" \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0' \
  -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' \
  -H 'Accept-Language: en-US,en;q=0.5' \
  -H 'Accept-Encoding: gzip, deflate' \
  https://www.doge.gov/api/receipts/overview | tr -d '\0')  # Remove null bytes

# Extract HTTP status code (last line of response)
http_status=$(echo "$response" | tail -n1)
json_data=$(echo "$response" | sed '$d')  # Remove last line (status code)

if [[ "$http_status" != "200" && "$http_status" != "201" ]]; then
  echo "Error: Received HTTP status code $http_status."
  exit 1
else
  echo "Success: HTTP $http_status. Processing data..."
fi

echo "$json_data" | jq .contracts > "${target}/doge_contracts_termination.json"
echo "$json_data" | jq .leases > "${target}/doge_leases_termination.json"

jq -r '(map(keys) | add | unique) as $cols | map(. as $row | $cols | map($row[.])) as $rows | $cols, $rows[] | @csv' "${target}/doge_contracts_termination.json" > "${target}/doge_contracts_termination.csv"
jq -r '(map(keys) | add | unique) as $cols | map(. as $row | $cols | map($row[.])) as $rows | $cols, $rows[] | @csv' "${target}/doge_leases_termination.json" > "${target}/doge_leases_termination.csv"

if command -v csvlint > /dev/null 2>&1 ; then
  echo "csvlint is installed."
  csvlint "${target}/doge_contracts_termination.csv"
  csvlint "${target}/doge_leases_termination.csv"
fi
