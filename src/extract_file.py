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
  
  import csv
from pathlib import Path
import subprocess
import sys
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def fetch_csv_data() -> list[dict]:
  """Track changed CSV file from Git and return its rows as a list of dicts."""
  dir_url = Path(__file__).resolve().parent
  root_dir = dir_url.parent
  sub_folder = root_dir / "storage"

  try:
    result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=AM", "HEAD~1", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
            cwd=root_dir
        )
        
  except (subprocess.CalledProcessError,FileNotFoundError):
    print("Log: No Git history or repository found.")
    return []

  changed_files = result.stdout.splitlines()

  csv_files = [
        sub_folder / Path(file).name
        for file in changed_files
        if file.endswith(".csv")
    ]

  if not csv_files:
    print("Log: No new CSV files detected in data/ folder.")
    return []

  print(f"Log: Detected new file: {csv_files[0].name}")

  with open(csv_files[0], mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)

  return data  
    




#_____________  
def main():
  file_data = fetch_csv_data()
  
if __name__=="__main__":
  main()