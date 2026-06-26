import streamlit as st

from dashboard import upload_page, get_conn
from analytics import analytics_page


st.set_page_config(page_title="FinAI Dashboard", layout="wide")

st.sidebar.title("📊 Navigation")

page = st.sidebar.radio(
    "Go to",
    ["📂 Upload CSV", "📈 Analytics Dashboard"]
)

if page == "📂 Upload CSV":
    upload_page()

elif page == "📈 Analytics Dashboard":
    conn = get_conn()
    analytics_page(conn)