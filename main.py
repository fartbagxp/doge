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
  script_contents = ""

  for script in soup.find_all("script"):
    if script.string:
      # Remove unwanted parts like self.__next_f.push( and \"])
      cleaned_script = re.sub(r'self\.__next_f\.push\(\[.*?,', '', script.string)
      cleaned_script = re.sub(r'\"]\)\s*\"', '', cleaned_script)
      script_contents += cleaned_script

  # Replace escaped quotes with actual quotes
  script_contents = script_contents.replace('\\"', '"')
  script_contents = script_contents.replace('\\', '')

  # Fix cases like ag"])"ency to create agency
  script_contents = re.sub(r'\"\]\)\"', '', script_contents)

  # Replace u0026 with &
  script_contents = script_contents.replace('u0026', '&')

  # Escape double quotes within the description field
  # script_contents = re.sub(r'(?<=description":")([^"]*?)(?<!\\)"([^"]*?)(?=")', r'\1\\"', script_contents)

  json_data.extend(json_pattern.findall(script_contents))

  return json_data

def process_json_data(json_data):
  contracts, grants, leases_termination = [], [], []
  for item in json_data:
    try:
      parsed = json.loads(item.replace("\\\"", "\""))
      if "fpds_status" in parsed:
        contracts.append(parsed)
      elif "sq_ft" in parsed:
        leases_termination.append(parsed)
      elif "agency" in parsed:
        grants.append(parsed)
    except json.JSONDecodeError:
      # print(item)
      continue
  return contracts, grants, leases_termination

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

def save_html(html, path):
  with open(path, "w", encoding="utf-8") as f:
    f.write(html)
    f.write("\n")

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
  contracts, grants, leases_termination = process_json_data(json_data)

  save_html(html, os.path.join(output_path, "doge_savings.html"))
  save_json(json_data, os.path.join(output_path, "html_parsed.json"))
  save_json(contracts, os.path.join(output_path, "doge_contracts_termination.json"))
  save_json(grants, os.path.join(output_path, "doge_grants_termination.json"))
  save_json(leases_termination, os.path.join(output_path, "doge_leases_termination.json"))
  save_csv(contracts, os.path.join(output_path, "doge_contracts_termination.csv"))
  save_csv(grants, os.path.join(output_path, "doge_grants_termination.csv"))
  save_csv(leases_termination, os.path.join(output_path, "doge_leases_termination.csv"))
  print(f"✅ Saved {len(contracts)} contracts, {len(grants)} grants, and {len(leases_termination)} lease termination to {output_path}")

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Fetch, parse, and save savings data.")
  parser.add_argument("output_path", type=str, help="Directory to save JSON and CSV files")
  args = parser.parse_args()
  main(args.output_path)
