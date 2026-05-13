import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))


import time
import asyncio
from connectors.redis_client import dequeue_job, set_job_status
from main import main_flow




async def worker():
    print("Worker started... listening for jobs")

    while True:
        # ✅ FIXED: aRedis call
        print("Listening")
        job = dequeue_job()

        if not job:
            time.sleep(1)
            continue

        job_id = job["job_id"]

        set_job_status(job_id, "processing")

        try:
            print(f"Processing job: {job_id}")

            await main_flow(job)

            set_job_status(job_id, "completed")
            print("Listening to new Activities") 
            

        except Exception as e:
            set_job_status(job_id, "failed")
            print("Worker error:", e)

        time.sleep(1)


if __name__ == "__main__":
    asyncio.run(worker())
  

