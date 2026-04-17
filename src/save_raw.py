import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import json
from pathlib import Path
import logging 
from datetime import datetime




logging.getLogger().setLevel(logging.INFO)


def save_raw_to_json(file):
  """Just saves our data to json for any emergency can be persisted to S3/R2"""
  
  folder_dir = Path(__file__).resolve().parent
  root_dir = folder_dir.parent
  storage = root_dir/"storage"
  storage.mkdir(parents=True, exist_ok=True)
  
  ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
  
  filename = f"raw_data_{ts}.json"
    
  file_path = storage/filename 
  
  try:
    with open(file_path,"w",encoding='utf-8') as f:
      json.dump(file,f,indent=4,ensure_ascii=False)
      logging.info("Raw Data saved")
  except Exception as e:
    logging.info(f"Count laod json error {e}")
    

