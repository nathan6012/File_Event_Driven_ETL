import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/api/upload/csv"

st.set_page_config(page_title="ETL Upload", layout="centered")

st.title("📂 CSV Upload")

uploaded_file = st.file_uploader("Choose CSV file", type=["csv"])

if uploaded_file:

    st.write("Selected file:", uploaded_file.name)

    # 👉 NO pandas, NO preview parsing
    file_bytes = uploaded_file.getvalue()

    if st.button("Upload"):

        files = {
            "file": (
                uploaded_file.name,
                file_bytes,
                "text/csv"
            )
        }

        try:
            response = requests.post(API_URL, files=files)

            if response.status_code == 201:
                st.success("Upload successful")
                st.json(response.json())

            else:
                st.error(f"Upload failed: {response.status_code}")
                st.text(response.text)

        except Exception as e:
            st.error(f"Connection error: {e}")