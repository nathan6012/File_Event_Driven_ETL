
from pydantic import BaseModel,Field, field_validator, ConfigDict
from decimal import Decimal
from datetime import datetime
from typing import Optional


import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class UserData(BaseModel):
  model_config = ConfigDict(extra="forbid")
  
  
  Customer_Name: str
  Age: int = Field(gt=15)
  Email: str
  Purchase_Amount: Decimal
  Purchase_Quantity: int
  Discount: Optional[Decimal]=None 
  Region: str  
  Purchase_Date: datetime
  
