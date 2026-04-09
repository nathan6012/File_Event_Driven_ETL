import pandas as pd
from pandas import json_normalize

import sys
import os
import logging 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
logging.getLogger().setLevel(logging.INFO)




def transform_data(clean,unclean):
  """ Tranforms/Normalizes Fro Bussiness Logic """
  pd.set_option("display.max_columns", None)
  pd.set_option("display.width", None)
  pd.set_option("display.max_colwidth", None)
  
  
  #Clean Fields
  df = pd.json_normalize(clean)
  #Unclean Fields 
  df1 = pd.json_normalize(unclean)
  
  
  
  df1["data.Customer_Name"] = df1["data.Customer_Name"].astype("str")
  
  df1["data.Age"] = pd.to_numeric(df1["data.Age"], errors="coerce")
  
  df1["data.Email"] = df1["data.Email"].astype("str")
  
  df1["data.Purchase_Amount"] = df1["data.Purchase_Amount"].astype("float")
  
  df1["data.Purchase_Quantity"] = df1["data.Purchase_Quantity"].astype("float")
  
  df1["data.Discount"] = (
    df1["data.Discount"]
    .astype("string")
    .str.replace("%", "", regex=False)
    .pipe(pd.to_numeric, errors="coerce"))
  
  

  df1["data.Region"] = df1["data.Region"].astype("str")
  
  df1["data.Purchase_Date"] = pd.to_datetime(df1["data.Purchase_Date"], errors="coerce")
  
  
  
  
  
  
  
  
  #Clean df

  df["data.Customer_Name"] = df["data.Customer_Name"].astype("str")
  
  df["data.Age"] = pd.to_numeric(df["data.Age"], errors="coerce")
  
  df["data.Email"] = df["data.Email"].astype("str")
  
  df["data.Purchase_Amount"] = df["data.Purchase_Amount"].astype("float")
  
  df["data.Purchase_Quantity"] = df["data.Purchase_Quantity"].astype("float")
  
  df["data.Discount"] = (
    df["data.Discount"]
    .astype("string")
    .str.replace("%", "", regex=False)
    .pipe(pd.to_numeric, errors="coerce"))
  

  df["data.Region"] = df["data.Region"].astype("str")
  
  df["data.Purchase_Date"] = pd.to_datetime(df["data.Purchase_Date"], errors="coerce")
  
  
  
  
  #Concat data 
  combined = pd.concat([df,df1])
  data = combined.set_index("idx").sort_index()
  
  for col in data.columns:
    data[col] = data[col].apply(
      lambda x: json.dumps(x) if isinstance(x, list) else x)
      
  data = data.drop_duplicates()
  data = data.reset_index()
  
  data= data.drop(columns=["errors","idx"])
  
  data.columns = data.columns.str.replace("data.","")
  
  
  
  
  #FillNa
  data["Customer_Name"] = data["Customer_Name"].fillna("Must have a name ")
  
  data["Age"] = data["Age"].fillna(0).astype("int32")
  
  
  data["Purchase_Amount"] = data["Purchase_Amount"].fillna(0).astype("float32")
  
  data["Purchase_Quantity"] = data["Purchase_Quantity"].fillna(0).astype("int32")

 # print(data["Purchase_Quantity"])
  data["Discount"]= data["Discount"].fillna(0).astype("float32")
  
  data['Purchase_Date'] = data['Purchase_Date'].fillna(pd.Timestamp('2026-01-01'))
  
  data['Email'] = data['Email'].where(data['Email'].str.strip() != '', 'NoEmail')
  
  data.columns = data.columns.str.lower()
  
  
  
  final_df = data.to_dict(orient='records')
  
  
  
  
  
  return final_df

  
def main():
  n = transform_data()

if __name__=="__main__":
  main()
  
  

