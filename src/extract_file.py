import csv
from pathlib import Path


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
 

# main Extract 
def fetch_csv_data():
  folder_dir = Path(__file__).resolve().parent
  root_dir = folder_dir.parent
  storage = root_dir / "storage"
  

  if not storage.exists():
    logging.info("Storage folder does not exist")
    return []

  csv_files = list(storage.glob("*.csv"))

  if not csv_files:
    logging.info("No CSV file found in storage")
    return []

    # Keep your "single file" behavior (like before)
  target_file_path = max(csv_files, key=lambda f: f.stat().st_mtime)


  data = []
  with open(target_file_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
      data.append(row)

  print(f"Loaded {len(data)} rows from {target_file_path.name}")


  return data  


  



#_____________  
def main():
  file_data = fetch_csv_data()
  
if __name__=="__main__":
  main()