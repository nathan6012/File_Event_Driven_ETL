import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))


import time
import asyncio
#from connectors.redis_client import dequeue_job, set_job_status
from main import main_flow


# 1. Import enqueue_job instead of the non-existent requeue_job
from connectors.redis_client import dequeue_job, set_job_status, enqueue_job

MAX_RETRIES = 2



import asyncio
from connectors.redis_client import dequeue_job, set_job_status, enqueue_job

MAX_RETRIES = 3

async def worker():
    print("Worker started... listening for jobs")
    while True:
        # Overwrites the same line instead of spamming down the terminal
        print("\rListening... ", end="", flush=True)
        
        job = dequeue_job() 
        if not job:
            continue
            
        # Clear the line when a job is found so logs don't overlap
        print("\r" + " " * 30 + "\r", end="", flush=True)
        
        job_id = job["job_id"]
        retries = job.get("retries", 0)
        
        if retries >= MAX_RETRIES:
            set_job_status(job_id, "dead_letter")
            print(f"Job {job_id} moved to DLQ (too many retries)")
            continue
            
        try:
            set_job_status(job_id, "processing")
            print(f"Processing job: {job_id}")
            
            await main_flow(job) 
            
            set_job_status(job_id, "completed")
            print("Job completed successfully")
            
        except Exception as e:
            retries += 1
            job["retries"] = retries
            print(f"Worker error: {e} | retry={retries}")
            
            if retries < MAX_RETRIES:
                set_job_status(job_id, "failed")
                enqueue_job(job) 
            else:
                set_job_status(job_id, "dead_letter")
                print(f"Job {job_id} reached max retries. Moved to DLQ.")
                
            await asyncio.sleep(1)







if __name__=="__main__":
    asyncio.run(worker())
    