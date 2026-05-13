import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import json
import pandas as pd
import aioboto3
from botocore.client import Config
from datetime import datetime
from io import BytesIO
from dotenv import load_dotenv


load_dotenv()



async def save_raw_to_r2(file):
    """Convert input → DataFrame → JSON → upload to R2"""

    session = aioboto3.Session()

    # =========================
    # Pandas conversion
    # =========================
    df = pd.DataFrame(file)

    json_data = df.to_json(orient="records", force_ascii=False, indent=4)

    # =========================
    # File naming
    # =========================
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    object_key = f"raw/raw_data_{ts}.json"

    # =========================
    # Upload to R2
    # =========================
    async with session.client(
        "s3",
        endpoint_url=os.getenv("R2_ENDPOINT_URL"),
        aws_access_key_id=os.getenv("R2_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("R2_SECRET_KEY"),
        config=Config(signature_version="s3v4"),
        region_name="auto"
    ) as s3:

        await s3.put_object(
            Bucket=os.getenv("R2_BUCKET_NAME"),
            Key=object_key,
            Body=json_data.encode("utf-8"),
            ContentType="application/json"
        )

    return object_key
