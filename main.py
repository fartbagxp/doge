import requests
import time
import json
import re
import os
import csv
import argparse
from bs4 import BeautifulSoup

def fetch_page(url, headers, max_retries=5, timeout=180):
  for attempt in range(1, max_retries + 1):
    try:
      response = requests.get(url, headers=headers, timeout=timeout)
      response.raise_for_status()
      return response.text
    except requests.RequestException as e:
      print(f"⚠️ Attempt {attempt} failed: {e}")
      if attempt < max_retries:
        time.sleep(2**attempt)
  print("❌ Failed after multiple attempts. Exiting.")
  exit(1)

def extract_json_from_html(html):
  soup = BeautifulSoup(html, "html.parser")
  json_pattern = re.compile(r"\{.*?\}")
  json_data = []
  
  for script in soup.find_all("script"):
    if script.string:
      json_data.extend(json_pattern.findall(script.string))
  
  return json_data

def process_json_data(json_data):
  savings, leases_termination = [], []
  for item in json_data:
    try:
      parsed = json.loads(item.replace("\\\"", "\""))
      if "date" in parsed and "agency" in parsed:
        if "sq_ft" in parsed:
          leases_termination.append(parsed)
        else:
          savings.append(parsed)
    except json.JSONDecodeError:
      continue
  return savings, leases_termination

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
  url = "https://doge.gov/savings"
  headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate"
  }

  os.makedirs(output_path, exist_ok=True)

  html = fetch_page(url, headers)
  json_data = extract_json_from_html(html)
  savings, leases_termination = process_json_data(json_data)

  save_json(savings, os.path.join(output_path, "doge_contracts_termination.json"))
  save_json(leases_termination, os.path.join(output_path, "doge_leases_termination.json"))
  save_csv(savings, os.path.join(output_path, "doge_contracts_termination.csv"))
  save_csv(leases_termination, os.path.join(output_path, "doge_leases_termination.csv"))

  print(f"✅ Saved {len(savings)} savings records and {len(leases_termination)} lease termination records to {output_path}")

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Fetch, parse, and save savings data.")
  parser.add_argument("output_path", type=str, help="Directory to save JSON and CSV files")
  args = parser.parse_args()
  main(args.output_path)
