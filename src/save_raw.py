import json
from pathlib import Path

import sys
import os
import logging 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

logging.getLogger().setLevel(logging.INFO)




def save_raw_to_json(file):
  """Just saves our data to json for any emergency can be persisted to S3/R2"""
  
  folder_dir = Path(__file__).resolve().parent
  root_dir = folder_dir.parent
  storage = root_dir/"storage"
  
  json_file = storage/"raw_data.json"
  
  
  with open(json_file,"w",encoding='utf-8') as f:
    json.dump(file,f,indent=4)
    logging.info("Raw Data saved")


    

def main():
  save_raw_to_json()

if __name__=="__main__":
  main()
  