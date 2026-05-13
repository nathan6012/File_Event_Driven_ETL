# streamlit_app.py

import streamlit as st
import requests

# =========================
# CONFIG
# =========================
API_URL = "http://127.0.0.1:8000/routers/upload/csv"

st.set_page_config(
    page_title=" ETL Upload",
    layout="centered"
)

# =========================
# UI
# =========================
st.title("📂 ETL File Upload")
st.write("Upload CSV files to FastAPI ETL pipeline")

uploaded_file = st.file_uploader(
    "Choose CSV File",
    type=["csv"]
)

# =========================
# UPLOAD BUTTON
# =========================
if uploaded_file is not None:

    st.success(f"Selected: {uploaded_file.name}")

    if st.button("Upload File"):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "text/csv"
            )
        }

        try:
            response = requests.post(API_URL, files=files)

            # SUCCESS
            if response.status_code == 201:
                st.success("✅ File uploaded successfully")
                st.json(response.json())

            # ERROR
            else:
                st.error(f"❌ Upload failed ({response.status_code})")
                st.json(response.json())

        except requests.exceptions.ConnectionError:
            st.error("❌ Could not connect to FastAPI server")