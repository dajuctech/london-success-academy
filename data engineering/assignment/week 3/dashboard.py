import streamlit as st
import pandas as pd
import plotly.express as px

# --- Load Data ---
df = pd.read_csv("assignment/week 3/data/novacart_sales.csv")

# --- Rename columns to match the brief ---
df = df.rename(columns={
    "medv":  "Median_s",
    "lstat": "por_OS",
    "rm":    "avg_no_it",
    "tax":   "TAX",
    "crim":  "Sale"
})

# --- Page Config ---
st.set_page_config(page_title="NovaCart Analytics", layout="wide")
st.title("NovaCart E-Commerce Analytics Dashboard")
st.caption("London Success Academy – Week 3 | Daniel Jude")

# --- Two Stakeholder Tabs ---
tab1, tab2 = st.tabs(["Sales Leadership View", "C-Suite Executive View"])

# =============================================
# TAB 1 – SALES LEADERSHIP VIEW
# =============================================
with tab1:
    st.subheader("Sales Performance Overview")

    # --- KPI Cards ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sellers", f"{len(df)}")
    col2.metric("Avg Items Per Sale", f"{df['avg_no_it'].mean():.2f}")
    col3.metric("Avg Sales Per Capita", f"{df['Sale'].mean():.2f}")

    st.divider()

    # --- Bar Chart: Top vs Bottom Sellers ---
    st.subheader("Seller Performance Comparison")

    top10    = df.nlargest(10, "Sale").copy()
    bottom10 = df.nsmallest(10, "Sale").copy()
    top10["Group"]    = "Top 10 Sellers"
    bottom10["Group"] = "Bottom 10 Sellers"

    import pandas as pd
    combined = pd.concat([top10, bottom10])
    combined["Seller"] = ["Seller " + str(i+1) for i in range(len(combined))]

    fig_bar = px.bar(
        combined, x="Seller", y="Sale", color="Group",
        title="Top 10 vs Bottom 10 Sellers by Sales Per Capita",
        labels={"Sale": "Sales Per Capita"},
        color_discrete_map={"Top 10 Sellers": "#2ecc71", "Bottom 10 Sellers": "#e74c3c"}
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()

    # --- Histogram: Sales Distribution ---
    st.subheader("Sales Distribution Across All Sellers")

    fig_hist = px.histogram(
        df, x="Sale", nbins=30,
        title="How Sales Per Capita Are Spread Across Sellers",
        labels={"Sale": "Sales Per Capita"},
        color_discrete_sequence=["#3498db"]
    )
    st.plotly_chart(fig_hist, use_container_width=True)

# =============================================
# TAB 2 – C-SUITE EXECUTIVE VIEW
# =============================================
with tab2:
    st.subheader("Executive Business Overview")

    # --- KPI Cards ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Median Business Value", f"£{df['Median_s'].median():,.0f}k")
    col2.metric("Avg Tax Rate", f"{df['TAX'].mean():,.0f} per 10k")
    col3.metric("Avg Market Competition", f"{df['por_OS'].mean():.1f}%")

    st.divider()

    # --- Scatter Plot: Tax vs Sales ---
    st.subheader("Tax Impact on Sales Revenue")

    fig_scatter = px.scatter(
        df, x="TAX", y="Sale",
        size="Median_s",
        color="por_OS",
        title="Tax Rate vs Sales Per Capita (bubble size = business value)",
        labels={
            "TAX":      "Tax Rate (per 10,000)",
            "Sale":     "Sales Per Capita",
            "por_OS":   "Other Sellers (%)",
            "Median_s": "Median Business Value"
        },
        color_continuous_scale="Reds"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.divider()

    # --- Seller Segments Pie Chart ---
    st.subheader("Seller Segments by Performance")

    df["Segment"] = pd.cut(
        df["Sale"],
        bins=[0, 5, 15, 30, 100],
        labels=["Needs Improvement", "Average", "Good", "Top Performer"]
    )

    fig_pie = px.pie(
        df, names="Segment",
        title="How Sellers Are Distributed Across Performance Segments",
        color_discrete_sequence=["#e74c3c", "#f39c12", "#3498db", "#2ecc71"]
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    st.divider()

    # --- Business Insight Callout ---
    st.subheader("Key Business Insight")
    st.info("Sellers in regions with tax rates above 400 per 10,000 show significantly lower sales per capita. Reducing tax burden in high-tax zones could unlock growth for underperforming sellers.")
