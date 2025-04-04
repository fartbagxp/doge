import os
import json
import csv
import argparse
from client import DogeClient

def save_json(data, path):
  with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

def save_csv(data, path):
  if data:
    keys = data[0].keys()
    with open(path, "w", encoding="utf-8", newline="") as f:
      writer = csv.DictWriter(f, fieldnames=keys)
      writer.writeheader()
      writer.writerows(data)

def main(output_path):
  os.makedirs(output_path, exist_ok=True)
  client = DogeClient()

  contracts = client.get_contract_savings()
  grants = client.get_grant_savings()
  leases = client.get_lease_savings()
  payments = client.get_payments()

  save_json(contracts, os.path.join(output_path, "doge_contracts_termination.json"))
  save_json(grants, os.path.join(output_path, "doge_grants_termination.json"))
  save_json(leases, os.path.join(output_path, "doge_leases_termination.json"))
  save_json(payments, os.path.join(output_path, "doge_payments_termination.json"))

  save_csv(contracts, os.path.join(output_path, "doge_contracts_termination.csv"))
  save_csv(grants, os.path.join(output_path, "doge_grants_termination.csv"))
  save_csv(leases, os.path.join(output_path, "doge_leases_termination.csv"))
  save_csv(payments, os.path.join(output_path, "doge_payments_termination.csv"))

  print(f"✅ Saved {len(contracts)} contracts, {len(grants)} grants, {len(leases)} leases, and {len(payments)} payments terminations to {output_path}")

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Fetch and save DOGE API savings data.")
  parser.add_argument("output_path", type=str, help="Directory to save JSON and CSV files")
  args = parser.parse_args()
  main(args.output_path)