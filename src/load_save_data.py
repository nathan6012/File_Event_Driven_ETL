#not set

from sqlalchemy.ext.asyncio import create_async_engine
import asyncio
from sqlalchemy import text,select,update 
#from sqlalchemy import inspect 
from sqlalchemy import Text,Float,inspect
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import UniqueConstraint 
from sqlalchemy import(Table,Column,Integer,String,MetaData,ForeignKey,Index,Numeric)

from sqlalchemy import DateTime

from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

load_dotenv()




async def load_to_postgres(data):
  """Loads The Transformed Data to Posgres Db"""
  
  db_url = os.getenv("DATABASE_URL").strip()
  
  engine = create_async_engine(db_url,echo=False)#echo=True)

  
  metadata = MetaData()
  
  customers = Table(
    "customers",
    metadata,

    Column("id", Integer, primary_key=True, autoincrement=True),

    Column("customer_name", String(100), nullable=False,unique=True),
    Column("age", Integer, nullable=False),
    Column("email", String(255), nullable=False),
    Column("purchase_amount", Numeric(10, 2), nullable=False),
    Column("purchase_quantity", Integer, nullable=False),
    Column("discount", Numeric(10, 2), nullable=True),
    Column("purchase_date", DateTime, nullable=False),)
    
  Index("id", customers.c.id)
  
  async with engine.begin() as conn:
    await conn.run_sync(metadata.create_all)
  

  async with engine.begin() as conn:
    stmt = insert(customers).values(data)
    stmt = stmt.on_conflict_do_update(
      index_elements=["customer_name"],
      
      set_={"age": stmt.excluded.age,
      
      "email": stmt.excluded.email,
      
      "purchase_amount": stmt.excluded.purchase_amount,
      
      "purchase_quantity": stmt.excluded.purchase_quantity,
      
      "discount": stmt.excluded.discount,
  
      "purchase_date":  stmt.excluded.purchase_date })
    await conn.execute(stmt)  
  
    
    
    
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
async def main():
  x = await load_to_postgres()

if __name__=="__main__":
  asyncio.run(main())
  
  
  
  
  
  
  



