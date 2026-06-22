import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import json
import logging


logging.getLogger().setLevel(logging.INFO)



def transform_data(clean, unclean):
    """ Transforms/Normalizes For Business Logic """
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)
    pd.set_option("display.max_colwidth", None)
    
    # --------------------------------------------------------
    # INITIALIZE DATAFRAMES SAFELY
    # --------------------------------------------------------
    df = pd.json_normalize(clean) if clean else pd.DataFrame()
    df1 = pd.json_normalize(unclean) if unclean else pd.DataFrame()
    
    # --------------------------------------------------------
    # UNCLEAN FIELDS PROCESSING (ONLY IF NOT EMPTY)
    # --------------------------------------------------------
    if not df1.empty:
        if "data.Customer_Name" in df1.columns:
            df1["data.Customer_Name"] = df1["data.Customer_Name"].astype("str")
        
        if "data.Age" in df1.columns:
            df1 = df1.drop(columns=["data.Age"])
        
        if "data.Email" in df1.columns:
            df1["data.Email"] = df1["data.Email"].astype("str")
        
        if "data.Purchase_Amount" in df1.columns:
            df1["data.Purchase_Amount"] = df1["data.Purchase_Amount"].astype("float")
        
        if "data.Purchase_Quantity" in df1.columns:
            df1["data.Purchase_Quantity"] = df1["data.Purchase_Quantity"].astype("float")
        
        if "data.Discount" in df1.columns:
            df1["data.Discount"] = (
                df1["data.Discount"]
                .astype("string")
                .str.replace("%", "", regex=False)
                .pipe(pd.to_numeric, errors="coerce")
            )
        
        if "data.Region" in df1.columns:
            df1["data.Region"] = df1["data.Region"].astype("str")
        
        if "data.Purchase_Date" in df1.columns:
            df1["data.Purchase_Date"] = pd.to_datetime(df1["data.Purchase_Date"], errors="coerce")
    
    # --------------------------------------------------------
    # CLEAN FIELDS PROCESSING (ONLY IF NOT EMPTY)
    # --------------------------------------------------------
    if not df.empty:
        if "data.Customer_Name" in df.columns:
            df["data.Customer_Name"] = df["data.Customer_Name"].astype("str")
        
        if "data.Age" in df.columns:
            df["data.Age"] = pd.to_numeric(df["data.Age"], errors="coerce")
            df = df.drop(columns=["data.Age"])
        
        if "data.Email" in df.columns:
            df["data.Email"] = df["data.Email"].astype("str")
        
        if "data.Purchase_Amount" in df.columns:
            df["data.Purchase_Amount"] = df["data.Purchase_Amount"].astype("float")
        
        if "data.Purchase_Quantity" in df.columns:
            df["data.Purchase_Quantity"] = df["data.Purchase_Quantity"].astype("float")
        
        if "data.Discount" in df.columns:
            df["data.Discount"] = (
                df["data.Discount"]
                .astype("string")
                .str.replace("%", "", regex=False)
                .pipe(pd.to_numeric, errors="coerce")
            )
        
        if "data.Region" in df.columns:
            df["data.Region"] = df["data.Region"].astype("str")
        
        if "data.Purchase_Date" in df.columns:
            df["data.Purchase_Date"] = pd.to_datetime(df["data.Purchase_Date"], errors="coerce")
            
    # --------------------------------------------------------
    # COMBINE DATA SAFELY
    # --------------------------------------------------------
    frames = [df for df in [df, df1] if not df.empty]
    
    if not frames:
        return []  # Return empty payload early if both clean and unclean datasets are completely empty
        
    combined = pd.concat(frames, ignore_index=True if "idx" not in frames[0].columns else False)
    
    if "idx" in combined.columns:
        data = combined.set_index("idx").sort_index().reset_index()
    else:
        data = combined

    # Serialize nested lists to JSON strings safely
    for col in data.columns:
        data[col] = data[col].apply(
            lambda x: json.dumps(x) if isinstance(x, list) else x
        )
        
    data = data.drop_duplicates()
    
    # Drop structural tracking columns if they exist
    cols_to_drop = [c for c in ["errors", "idx"] if c in data.columns]
    if cols_to_drop:
        data = data.drop(columns=cols_to_drop)
    
    # Strip nested data. prefix layout
    data.columns = data.columns.str.replace("data.", "", regex=False)
    
    # --------------------------------------------------------
    # FALLBACK FILLING, VALIDATION, AND CASTING
    # --------------------------------------------------------
    if "Customer_Name" in data.columns:
        data["Customer_Name"] = data["Customer_Name"].fillna("Must have a name ")
    else:
        data["Customer_Name"] = "Must have a name "
        
    if "Purchase_Amount" in data.columns:
        data["Purchase_Amount"] = data["Purchase_Amount"].fillna(0)
    else:
        data["Purchase_Amount"] = 0.0

    if "Purchase_Quantity" in data.columns:
        data["Purchase_Quantity"] = data["Purchase_Quantity"].fillna(0)
    else:
        data["Purchase_Quantity"] = 0

    # Drop rows with nulls in target critical data metrics
    intersect_cols = [c for c in ["Purchase_Amount", "Purchase_Quantity"] if c in data.columns]
    if intersect_cols:
        data = data.dropna(subset=intersect_cols)
    
    # Strict datatype casting for target DB configuration contract
    data["Purchase_Amount"] = data["Purchase_Amount"].astype("float32")
    data["Purchase_Quantity"] = data["Purchase_Quantity"].astype("int32")

    if "Discount" in data.columns:
        data["Discount"] = data["Discount"].fillna(0).astype("float32")
    else:
        data["Discount"] = 0.0
        
    if "Purchase_Date" in data.columns:
        data['Purchase_Date'] = data['Purchase_Date'].fillna(pd.Timestamp('2026-01-01'))
    else:
        data['Purchase_Date'] = pd.Timestamp('2026-01-01')
        
    if "Email" in data.columns:
        data['Email'] = data['Email'].fillna('NoEmail')
        data['Email'] = data['Email'].where(data['Email'].astype(str).str.strip() != '', 'NoEmail')
    else:
        data['Email'] = 'NoEmail'
    
    # Normalize database target casing layout structure
    data.columns = data.columns.str.lower()
    
    if "email" in data.columns:
        data["email"] = data["email"].astype(str).str.replace(r"\.(?=[^@]*@)", "", regex=True)
    
    if "region" in data.columns:
        data = data.drop(columns=["region"])
    
    return data.to_dict(orient='records')
