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

  result = subprocess.run(
        ["git", "ls-files", "--modified", "--others", "--exclude-standard"],
        capture_output=True,
        text=True,
        check=True,
        cwd=root_dir  
    )
    
  changed_files = result.stdout.splitlines()

  target_file_path = None
  for file_path_str in changed_files:
    absolute_path = root_dir / file_path_str
    
    if absolute_path.suffix == ".csv" and storage_dir in absolute_path.parents:
      
      if absolute_path.exists():
        target_file_path = absolute_path
        break
    
  if not target_file_path:
    print("No CSV file detected in storage")
    return []  
  
    # 2. Your original read logic restored
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