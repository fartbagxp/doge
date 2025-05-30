import argparse
import csv
import json
import os
import sys

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
  payments_stats = client.get_payments_statistics()

  if len(contracts) == 0:
    print("No contract terminations found.")
  if len(grants) == 0:
    print("No grant terminations found.")
  if len(leases) == 0:
    print("No lease terminations found.")
  if len(payments) == 0:
    print("No payment terminations found.")
  if len(contracts) == 0 or len(grants) == 0 or len(leases) == 0 or len(payments) == 0 or len(payments_stats) == 0:
    print("Error fetching data from the DOGE API. Please check the API status or your network connection.")
    return

  # Heuristic checks for unusual data, ex. if records were deleted, 
  # we should guard against updating
  heuristic_error = ""
  if len(contracts) < 10000:
    heuristic_error += "The number of contracts is less than 10,000, which is unusual.\n"
  if len(grants) < 15000:
    heuristic_error += "The number of grants is less than 15,000, which is unusual.\n"
  if len(leases) < 450:
    heuristic_error += "The number of leases is less than 450, which is unusual.\n"
  if len(payments) < 100000:
    heuristic_error += "The number of payments is less than 100,000, which is unusual.\n"
  if heuristic_error != "":
    print("Heuristic error detected:")
    print(heuristic_error)
    print("Please verify the data integrity before proceeding.")
    sys.exit(1)

  save_json(contracts, os.path.join(output_path, "doge_contracts_termination.json"))
  save_json(grants, os.path.join(output_path, "doge_grants_termination.json"))
  save_json(leases, os.path.join(output_path, "doge_leases_termination.json"))
  save_json(payments, os.path.join(output_path, "doge_payments.json"))
  save_json(payments_stats, os.path.join(output_path, "doge_payments_statistics.json"))

  save_csv(contracts, os.path.join(output_path, "doge_contracts_termination.csv"))
  save_csv(grants, os.path.join(output_path, "doge_grants_termination.csv"))
  save_csv(leases, os.path.join(output_path, "doge_leases_termination.csv"))
  save_csv(payments, os.path.join(output_path, "doge_payments.csv"))
  save_csv(payments_stats, os.path.join(output_path, "doge_payments_statistics.csv"))

  print(f"✅ Saved {len(contracts)} contracts, {len(grants)} grants, {len(leases)} leases, {len(payments)} payments, and {len(payments_stats)} payment statistics to {output_path}")

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Fetch and save DOGE API savings data.")
  parser.add_argument("output_path", type=str, help="Directory to save JSON and CSV files")
  args = parser.parse_args()
  main(args.output_path)