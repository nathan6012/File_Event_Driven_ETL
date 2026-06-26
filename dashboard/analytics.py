import streamlit as st

from charts import sales_performance
from sqlalchemy import text
from charts import sales_performance

# -------------------------
# KPI FUNCTIONS (your existing ones)
# -------------------------

def total_customers(conn):
    return conn.execute(text("""
        SELECT COUNT(customer_name)
        FROM dem_sales_customers
    """)).scalar() or 0


def total_revenue(conn):
    return conn.execute(text("""
        SELECT SUM(purchase_amount)
        FROM facts_sales
    """)).scalar() or 0


def total_orders(conn):
    return conn.execute(text("""
        SELECT COUNT(*)
        FROM facts_sales
    """)).scalar() or 0


def quantity_sold(conn):
    return conn.execute(text("""
        SELECT SUM(purchase_quantity)
        FROM facts_sales
    """)).scalar() or 0


def discount_given(conn):
    return conn.execute(text("""
        SELECT 
            COALESCE(
                SUM(discount) * 100.0 / NULLIF(SUM(purchase_amount), 0),
                0
            )
    """)).scalar() or 0


# -------------------------
# MAIN ANALYTICS PAGE
# -------------------------

def analytics_page(conn):

    st.title("📊 Analytics Dashboard")

    # ---------------- KPIs ----------------
    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Customers", total_customers(conn))
    col2.metric("Revenue", total_revenue(conn))
    col3.metric("Orders", total_orders(conn))
    col4.metric("Quantity", quantity_sold(conn))
    col5.metric("Discount %", discount_given(conn))

    st.divider()

    # ---------------- CHARTS ----------------
    st.subheader("📈 Sales Charts")

    # 👉 Get data from DB for charts
    result = conn.execute(text("""
        SELECT 
            date_id,
            purchase_amount,
            purchase_quantity,
            discount
        FROM facts_sales
    """))

    data = [dict(row._mapping) for row in result]

    # Call chart function
    if data:
        sales_performance(data)
    else:
        st.info("No data available for charts")