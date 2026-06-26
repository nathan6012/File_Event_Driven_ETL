#add
import pandas as pd
import plotly.express as px


def sales_performance(data):
    df = pd.DataFrame(data).copy()

    # Ensure numeric safety
    df["purchase_amount"] = pd.to_numeric(df["purchase_amount"])
    df["purchase_quantity"] = pd.to_numeric(df["purchase_quantity"])
    df["discount"] = pd.to_numeric(df["discount"])

    # -----------------------------
    # 1. REVENUE BY DATE (BAR)
    # -----------------------------
    revenue_df = df.groupby("date_id", as_index=False)["purchase_amount"].sum()

    fig1 = px.bar(
        revenue_df,
        x="date_id",
        y="purchase_amount",
        title="Revenue by Date",
        text="purchase_amount"
    )
    fig1.update_traces(textposition="outside")
    fig1.show()

    # -----------------------------
    # 2. QUANTITY BY DATE (BAR)
    # -----------------------------
    qty_df = df.groupby("date_id", as_index=False)["purchase_quantity"].sum()

    fig2 = px.bar(
        qty_df,
        x="date_id",
        y="purchase_quantity",
        title="Quantity Sold by Date",
        text="purchase_quantity"
    )
    fig2.update_traces(textposition="outside")
    fig2.show()

    # -----------------------------
    # 3. DISCOUNT vs NET VALUE (PIE)
    # -----------------------------
    total_discount = df["discount"].sum()
    total_revenue = df["purchase_amount"].sum()

    pie_df = pd.DataFrame({
        "type": ["Revenue", "Discount"],
        "value": [total_revenue, total_discount]
    })

    fig3 = px.pie(
        pie_df,
        names="type",
        values="value",
        title="Revenue vs Discount Impact"
    )
    fig3.show()