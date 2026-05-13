import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import asyncio
from dotenv import load_dotenv
import pandas as pd


from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import (
    Table, Column, Integer, String, MetaData,
    Numeric, DateTime, Index
)
from sqlalchemy.dialects.postgresql import insert


load_dotenv()


# -----------------------------
# STRICT DB SCHEMA CONTRACT
# -----------------------------
ALLOWED_COLUMNS = {
    "customer_name",
    "email",
    "purchase_amount",
    "purchase_quantity",
    "discount",
    "purchase_date"
}


async def load_to_postgres(data):
    """Loads Transformed Data into PostgreSQL safely"""

    db_url = os.getenv("DATABASE_URL").strip()
    engine = create_async_engine(db_url, echo=False)

    metadata = MetaData()

    sales = Table(
        "sales",
        metadata,

        Column("id", Integer, primary_key=True, autoincrement=True),

        Column("customer_name", String(50), nullable=False, unique=True),
        Column("email", String(50), nullable=False),
        Column("purchase_amount", Numeric(10, 2), nullable=False),
        Column("purchase_quantity", Integer, nullable=False),
        Column("discount", Numeric(10, 2), nullable=True),
        Column("purchase_date", DateTime, nullable=False),
    )

    Index("id_index", sales.c.id)

    # -----------------------------
    # CREATE TABLE IF NOT EXISTS
    # -----------------------------
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    # -----------------------------
    # SAFE DATA CLEANING BEFORE INSERT
    # -----------------------------
    clean_data = []

    for row in data:
        filtered_row = {k: v for k, v in row.items() if k in ALLOWED_COLUMNS}

        # Ensure all required columns exist
        for col in ALLOWED_COLUMNS:
            filtered_row.setdefault(col, None)
            
            # Explicitly turn Pandas NaT into None so SQLAlchemy doesn't choke
            if filtered_row[col] is pd.NaT:
                filtered_row[col] = None

        clean_data.append(filtered_row)

    # Return early if there is no data to insert to prevent empty query execution
    if not clean_data:
        await engine.dispose()
        return

    # -----------------------------
    # INSERT + UPSERT (FIXED)
    # -----------------------------
    async with engine.begin() as conn:
        # 1. Define the structural insert statement without embedding the data payload
        stmt = insert(sales)

        # 2. Wire the conflict behavior targeting your unique index column
        stmt = stmt.on_conflict_do_update(
            index_elements=["customer_name"],
            set_={
                "email": stmt.excluded.email,
                "purchase_amount": stmt.excluded.purchase_amount,
                "purchase_quantity": stmt.excluded.purchase_quantity,
                "discount": stmt.excluded.discount,
                "purchase_date": stmt.excluded.purchase_date,
            }
        )

        # 3. Pass clean_data list directly to execution for native multi-row binding
        await conn.execute(stmt, clean_data)

    await engine.dispose()






if __name__ == "__main__":
    asyncio.run(main())
  
  
  
  
  
  
  
  
  



