from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import pandas as pd
import uuid




from connectors.redis_client import enqueue_job, set_job_status  # redis 


router = APIRouter()
# =========================
# SAVE FILE
# =========================
def save_file(file: UploadFile) -> Path:
    base_path = Path(__file__).resolve().parent
    base_root = base_path.parent 
    storage_dir = base_root / "storage"
    storage_dir.mkdir(parents=True, exist_ok=True)

    # safe unique filename
    safe_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = storage_dir / safe_filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path


# =========================
# CSV UPLOAD ROUTE
# =========================
@router.post("/upload/csv", status_code=201)
async def upload_csv(file: UploadFile = File(...)):

    # validate extension
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files accepted")

    try:
        file_path = save_file(file)
        
        job_id = str(uuid.uuid4())

        # 3. Initial status
        set_job_status(job_id, "queued")
        # 4. Enqueue job for worker
        job = {
            "job_id": job_id,
            "type": "csv_ingestion",
            "file_path": str(file_path),
            "original_filename": file.filename
        }

        enqueue_job(job)
 
        

        # read preview (first rows)
        df = pd.read_csv(file_path)
        preview = df.head(5).to_dict(orient="records")

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"CSV processing failed: {str(e)}"
        )

    return {
        "status": "success",
        "file_name": file.filename,
        "stored_path": str(file_path),
        "preview": preview
    }