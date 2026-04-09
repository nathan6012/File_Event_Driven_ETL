#not set yet
from prefect import flow, task,get_run_logger
import asyncio

from extract_file import fetch_csv_data
from save_raw import save_raw_to_json
from validate_data import validate_file_data
from transform_data import transform_data
from load_save_data import load_to_postgres
from models import UserData





import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@task(retries=3,log_prints=True)
def fetch_file_task():
  
  return fetch_csv_data()
  
  
@task(log_prints=True)
def save_raw_data_task(file):
  
  return save_raw_to_json(file)
  
  
@task(log_prints=True)
def validate_data_task(data,Model):
  
  return validate_file_data(data,Model)

@task(log_prints=True)
def transform_data_task(clean,unclean):
  
  return transform_data(clean,unclean)

@task(retries=3,log_prints=True)
async def load_to_db_task(data1):
  
  return await load_to_postgres(data1)
  








  
@flow(name="File_Event_Driven_Flow",retries=3,log_prints=True)
async def main_flow():
  file = fetch_csv_data()
  print(len(file))
  
  save_raw_to_json(file)
  
  clean,unclean = validate_file_data(file,UserData)
  
  data1= transform_data(clean,unclean)
  
  await load_to_postgres(data1)

if __name__=="__main__":
  asyncio.run(main_flow())
  
  
