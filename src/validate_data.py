from pydantic import BaseModel, ValidationError, Field, field_validator, ConfigDict
from decimal import Decimal
from datetime import datetime
from typing import Optional
import json

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def validate_file_data(data,Model):
  clean = []
  unclean = []
  for idx,records in enumerate(data):
    #Our clean Data 
    try:
      valid = Model(**records)
      clean.append({
        "idx":idx,
        "data":valid.model_dump(mode="json")})
    #Our Not clean Data Logic     
        
    except ValidationError as e:
      unclean.append({
        "idx":idx,
        "data":records,
          "errors": e.errors()
    
      })
      
  return clean,unclean
  
  

def main():
  validate_file_data()

if __name__=="__main__":
  main()
  
  
