
# 📊 Event-Driven CSV File ETL

![Python](https://img.shields.io/badge/Language-Python-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi&logoColor=white)
![Redis](https://img.shields.io/badge/Cache-Redis-DC382D?logo=redis&logoColor=white)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Prefect](https://img.shields.io/badge/Orchestration-Prefect-06b6d4)
![Pandas](https://img.shields.io/badge/Data-Pandas-black)
![SQLAlchemy](https://img.shields.io/badge/Database-SQLAlchemy-red)
![Cloudflare R2](https://img.shields.io/badge/Storage-Cloudflare%20R2-F38020?logo=cloudflare&logoColor=white)
![Neon PostgreSQL](https://img.shields.io/badge/Storage-Neon%20PostgreSQL-00E599?logo=postgresql&logoColor=white)


---

#🚀 Event-Driven ETL Platform (FastAPI + Redis + Streamlit)

#📌 Project Overview

This project is a real-time, event-driven ETL system that allows end users to simply drop or upload CSV files, which are then automatically processed through a full data pipeline.

The system combines:

FastAPI → file ingestion API layer

Redis → event queue / job triggering system

ETL Pipeline (Python) → extract, validate, transform, load

Streamlit Dashboard → Enduser data upload 

Slack Notifications → real-time pipeline status alerts


Once a file is received, the system automatically triggers an ETL workflow that processes the data and makes it available for analytics.


---

##🎯 Problem It Solves

In many real-world scenarios:

Users upload inconsistent CSV files
Data arrives from multiple sources
Manual cleaning is slow and error-prone
Teams lack real-time visibility into processing status

This system solves that by:

> Turning file uploads into an automated, event-driven data pipeline with real-time processing, validation, and monitoring from file to Database and Cloud  and analytics Ready Data 




---

⚙️ System Architecture

🧩 Core Flow

User Uploads File (FastAPI)
        ↓
Redis Queue (Event Trigger)
        ↓
ETL Worker (Redis Worker)
        ↓
Extract → Validate → Transform
        ↓
Save Raw JSON (Audit Layer)
        ↓
Load Processed Data (Storage / DB)
        ↓
Slack Notification (Success / Failure)
        ↓
Streamlit Dashboard (Visualization)


---

🏗️ Project Structure

.
├── app/
│   ├── api.py              # FastAPI entry points
│   ├── routers.py          # Upload & endpoints
│
├── connectors/
│   ├── redis_client.py     # Redis connection + queue handling
│
├── dashboard/
│   ├── dashboard.py        # Streamlit UI for analytics
│
├── src/
│   ├── extract_file.py     # File ingestion logic
│   ├── validate_data.py    # Schema validation (Pydantic)
│   ├── transform_data.py   # Data cleaning (Pandas)
│   ├── load_save_data.py   # Load processed data
│   ├── save_raw.py         # Raw JSON archival layer
│   ├── redis_worker.py    # ETL worker consuming Redis jobs
│   ├── models.py           # Data schemas
│   ├── main.py             # Pipeline entry orchestration
│
├── utils/
│   ├── notifier.py         # Slack notifications
│   ├── cleanup.py          # Storage cleanup job
│
├── storage/                # Raw + processed file storage layer
│
├── sql/
│   ├── models.sql          # Database schema
│
├── tests/
│   ├── test_extract.py
│   ├── test_load_save.py
│   ├── test_save_raw.py
│
├── requirements.txt
└── README.md


---

✨ Key Features

⚡ Event-Driven Architecture

File upload triggers Redis event

Worker processes ETL automatically


🧼 Data Processing Pipeline

Extract raw CSV files

Validate using Pydantic schemas

Transform using Pandas

Load into structured storage/database


💾 Raw Data Archiving

Every input file is saved as JSON

Ensures traceability and audit logs


📊 Dashboard (Streamlit)

View processed datasets

Monitor pipeline status


🔔 Real-Time Notifications

Slack alerts for:

ETL success

ETL failure

system errors



⚙️ Background Processing

Redis worker handles async ETL execution

Prevents blocking API requests



---

🚀 Business Value (Why this matters)

This system simulates real-world data engineering problems:

✔ Solves:

Manual data cleaning workflows

Delayed batch processing systems

Lack of pipeline visibility

Poor data quality control

No real-time feedback on ingestion



---

🧠 What Makes This Project Strong

This is not just ETL — it is a:

> 🟢 Mini Data Platform with Event-Driven Architecture



##It demonstrates:

Backend engineering (FastAPI)

Distributed systems thinking (Redis queues)

Data engineering (ETL pipelines)

Data validation (Pydantic)

Observability (Slack alerts)

Analytics layer (Streamlit dashboard)



---

##🔁 ETL Pipeline Stages

1. Extract

CSV file ingestion

2. Validate

Schema enforcement (Pydantic)

3. Transform

Cleaning, deduplication, formatting

4. Load
Store processed data/ Posgtresql

5. Audit

Save raw JSON snapshot to R2

---

##🔔 Notification System

The system sends Slack alerts for:

✅ ETL Success

❌ ETL Failure

⚠️ Processing Errors
---

📊 Dashboard

Streamlit dashboard provides:
UI for User to uplaod Data 

---

##🧰 Tech Stack

Tool	Purpose

FastAPI	API ingestion layer
Redis	Event queue system
Python	Core ETL logic
Pandas	Data transformation
Pydantic	Schema validation
Streamlit	Dashboard UI
Slack API	Notifications
SQL	Data storage layer



---

🧪 Testing

pytest


---

📌 Future Improvements

Add data versioning system

Add role-based dashboard access

Add observability (logs + metrics + tracing)



---

🏁 Summary

This project is a:

> Real-time event-driven ETL system combining FastAPI, Redis, Streamlit, and automated data validation pipelines.

Usage 
create Venv add R2 Credentials and Database in .env 

git clone https://github.com/nathan6012/File_Event_Driven_ETL.git

cd to :/ root folder 
  run in terminal (root)
  uvicorn app.api:app --host 0.0.0.0 --port 8000
  redis-server 
  streamlit run dashboard/dashboard.py
  then Open Chrome/ and upload file 
  
  note: all services / servers must be running 
  api,streamlit,redis server and  redis_worker 
  # run workflow / see workflow  
  python src/redis_worker.py
  
  note : the worker wi remain listing for any Activities from the api 
  



