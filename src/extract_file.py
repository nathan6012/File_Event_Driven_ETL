import csv
from pathlib import Path
import subprocess

import sys
import os
import logging 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
#Logging 
logging.getLogger().setLevel(logging.INFO)





def fetch_csv_data()-> dict[str,list[dict]]:
  """ Tracks Git hub /Storage to process CSV files that are commited in that folder in ETL pipeline"""
  
  folder_dir = Path(__file__).resolve().parent
  root_dir = folder_dir.parent
  storage = root_dir/"storage"
  # Create file dir  does not exist 
  storage.mkdir(parents=True, exist_ok=True)
 # print(storage)
  try:
    subprocess.run(
      ["git", "diff", "--name-only", "--diff-filter=AM", "HEAD~1", "HEAD"],
    capture_output=True,
            text=True,
            check=True,
            cwd=root_dir
      )
  except (subprocess.CalledProcessError, FileNotFoundError):
    logging.info("No git History found")
    
    return {}
    
    
    
  new_files = result.stdout.splitlines()
  csv_files = [
        storage/ Path(file).name
        for file in new_files
        if file.endswith(".csv")
    ]
    
  if not csv_files:
    print("No Files Found")
    return {}
  
  all_data:dict[str, list[dict]]  = {}
  
  for path in csv_files:
    if path.exists():
      print(f"Log: Reading file: {path.name}")
      
      with open(path,"r", encoding="utf-8") as file:
        
        reader = csv.DictReader(file)
        all_data[path.name] = list(reader)
        

  return all_data







#_____________  
def main():
  file_data = fetch_csv_data()
  
if __name__=="__main__":
  main()