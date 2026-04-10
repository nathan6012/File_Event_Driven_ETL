import csv
from pathlib import Path
import subprocess
import sys
import os
import logging 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
#Logging 
logging.getLogger().setLevel(logging.INFO)

# Set up logging
logging.basicConfig(level=logging.INFO)



def fetch_csv_data():
  
  folder_dir = Path(__file__).resolve().parent
  root_dir = folder_dir.parent
  storage = root_dir/"storage"
  #file = storage/"sample_data.csv"

  
  target_file_path = None
    
    # List all files in the storage folder
  if storage.exists():
    for file in storage.glob("*.csv"):
      target_file_path = file
      break
    
  if not target_file_path:
    print("No CSV file found in storage")
    if storage.exists():
      print("Contents of storage")
      
      return []  
  
    # 3. Your original read logic restored exactly
  with open(target_file_path, "r", newline="", encoding="utf-8") as f:
    data = []
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