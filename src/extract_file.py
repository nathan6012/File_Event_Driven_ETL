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



def fetch_csv_data() -> list[dict]:
  
  folder_dir = Path(__file__).resolve().parent
  root_dir = folder_dir.parent
  storage = root_dir/"storage"
  #file = storage/"sample_data.csv"
  
  result = subprocess.run(
        ["git", "ls-files", "--modified", "--others", "--exclude-standard"],
        capture_output=True,
        text=True,
        check=True
    )
  changed_files = result.stdout.splitlines()

    # 3. Find first CSV inside storage/
  target_file = None
  
  for file in changed_files:
    full_path = Path(file)

    if full_path.suffix == ".csv":
      target_file = full_path
      break
    
  if not target_file:
    print("No CSV file detected")
    return []  
  
  
      
  file_path = storage / target_file.name  
  
  with open(file_path, "r", newline="", encoding="utf-8") as f:
    data = []
    reader = csv.DictReader(f)

    for row in reader:
      data.append(row)
  
  print(f"Loaded {len(data)} rows from {file_path.name}")    
  
  return data    

  



#_____________  
def main():
  file_data = fetch_csv_data()
  
if __name__=="__main__":
  main()