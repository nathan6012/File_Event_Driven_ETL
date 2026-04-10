import csv
from pathlib import Path
import subprocess
import sys
import json
import os
import logging 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
#Logging 
logging.getLogger().setLevel(logging.INFO)

# Set up logging
logging.basicConfig(level=logging.INFO)

#Helper Load 
def load_registry(registry_path):
  if not registry_path.exists():
    return {"processed": []}

  if registry_path.stat().st_size == 0:
    return {"processed": []}

  try:
    with open(registry_path, "r", encoding="utf-8") as f:
      return json.load(f)

  except json.JSONDecodeError:
    return {"processed": []}
    

#Helper save 
def save_registry(registry_path, data):
  with open(registry_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
    
    
    

# main Extract 
def fetch_csv_data():
  folder_dir = Path(__file__).resolve().parent
  root_dir = folder_dir.parent
  storage = root_dir / "storage"
  
  registry_path = storage / "processed_files.json"

    # ----------------------------
    # LOAD REGISTRY
    # ----------------------------
  registry = load_registry(registry_path)
  processed_files = set(registry["processed"])

  if not storage.exists():
    logging.info("Storage folder does not exist")
    return []

  csv_files = list(storage.glob("*.csv"))

  if not csv_files:
    logging.info("No CSV file found in storage")
    return []

    # ----------------------------
    # FIND NEW FILE
    # ----------------------------
  target_file_path = None

  for file in csv_files:
    if file.name not in processed_files:
      target_file_path = file
      break

  if not target_file_path:
    print("No NEW files to process")
    return []

    # ----------------------------
    # READ FILE
    # ----------------------------
  data = []

  with open(target_file_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
      data.append(row)

  print(f"Loaded {len(data)} rows from {target_file_path.name}")

    # ----------------------------
    # UPDATE REGISTRY
    # ----------------------------
  registry["processed"].append(target_file_path.name)
  save_registry(registry_path, registry)

  return data  


  



#_____________  
def main():
  file_data = fetch_csv_data()
  
if __name__=="__main__":
  main()