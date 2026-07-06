# app redis client 
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import json
import os
from dotenv import load_dotenv
from redis import Redis   # 🔥 SWITCHED TO SYNC

# =========================
# LOAD ENV
# =========================
load_dotenv()

# =========================
# ASYNC REDIS CLIENT
# =========================
redis_client = Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True,
    socket_connect_timeout=5,
)

QUEUE_NAME = "etl_jobs"


# =========================
# ENQUEUE JOB (ASYNC)
# =========================
def enqueue_job(job: dict):
    redis_client.lpush(QUEUE_NAME, json.dumps(job))


# =========================
# DEQUEUE JOB (ASYNC)
# =========================
def dequeue_job():
    item = redis_client.brpop(QUEUE_NAME, timeout=5)

    if item is None:
        return None

    _, job = item
    return json.loads(job)


# =========================
# JOB STATUS HELPERS (ASYNC)
# =========================
def set_job_status(job_id: str, status: str):
    redis_client.set(f"job:{job_id}:status", status)


def get_job_status(job_id: str):
    return redis_client.get(f"job:{job_id}:status")