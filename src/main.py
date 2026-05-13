import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from prefect import flow, task
import asyncio

from extract_file import fetch_csv_data
from save_raw import save_raw_to_r2
from validate_data import validate_file_data
from transform_data import transform_data
from load_save_data import load_to_postgres
from models import UserData

from utils.notifier import send_etl_success, send_etl_failure
from utils.cleanup import delete_old_files


# =========================
# TASKS
# =========================

@task(retries=3, log_prints=True)
def fetch_file_task():
    return fetch_csv_data()


@task(log_prints=True)
async def save_raw_data_task(file):
    return await save_raw_to_r2(file)


@task(log_prints=True)
def validate_data_task(data, Model):
    return validate_file_data(data, Model)


@task(log_prints=True)
def transform_data_task(clean, unclean):
    return transform_data(clean, unclean)


@task(retries=3, log_prints=True)
async def load_to_db_task(data):
    return await load_to_postgres(data)


@task(retries=3, log_prints=True)
def delete_old_files_task():
    return delete_old_files()


# =========================
# FLOW
# =========================

@flow(name="File_Event_Driven_Flow", retries=3, log_prints=True)
async def main_flow(job: dict):

    print(f"Processing job: {job['job_id']}")

    file_path = job["file_path"]

    try:
        # 1. EXTRACT (fail fast ok)
        file = fetch_file_task()
        print(f"Extracted: {len(file)} records")

        # 2. SAVE RAW (non-critical → safe)
        try:
            await save_raw_data_task(file)
        except Exception as e:
            print(f"⚠ Raw save failed (ignored): {e}")

        # 3. VALIDATE (critical but safe output expected)
        clean, unclean = validate_data_task(file, UserData)
        print(f"Clean: {len(clean)} | Unclean: {len(unclean)}")

        # 4. TRANSFORM (critical)
        data1 = transform_data_task(clean, unclean)

        # 5. LOAD (MOST IMPORTANT FIX HERE)
        try:
          
            await load_to_db_task(data1)
            
            send_etl_success(
            job_id=job["job_id"],
            file_path=file_path,
            data=len(data1)
        )

            print("LOAD SUCCESS")
            print("ETL COMPLETE")

        except Exception as load_error:

            # ❗ DO NOT FAIL ENTIRE FLOW
            print(f"❌ Load failed but ETL continues: {load_error}")

            send_etl_failure(
                job_id=job["job_id"],
                error=f"LOAD_ERROR: {str(load_error)}"
            )

        # 6. CLEANUP (always run)
        try:
            delete_old_files_task()
            print("Files Checked")
        except Exception as e:
            print("⚠ Cleanup failed:")

        

    except Exception as e:

        # only true system-level failure ends here
        send_etl_failure(
            job_id=job["job_id"],
            error=f"PIPELINE_CRASH:{len(e)}")

        print(f"ETL FAILED: {e}")

        # still raise for Prefect visibility
        raise