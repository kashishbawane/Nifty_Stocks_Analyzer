# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="📊 Nifty Stock Analysis Dashboard", layout="wide")
st.title("📊 Nifty Stock Analysis Dashboard with SMA50 & SMA200")

# ----------------------
# Load Dataset
# ----------------------
uploaded_file = st.file_uploader("Upload your Nifty Stock dataset (CSV)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Show preview
    st.subheader("🔎 Data Preview")
    st.dataframe(df.head())

    # ----------------------
    # Fix Date Column Safely
    # ----------------------
    if "Date" not in df.columns:
        st.error("❌ 'Date' column not found in dataset!")
        st.stop()

    # Safe conversion: invalid dates → NaT
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Drop invalid dates
    df = df.dropna(subset=["Date"])

    # ----------------------
    # Clean Stock column
    # ----------------------
    if "Stock" in df.columns:
        df["Stock"] = df["Stock"].astype(str).str.strip().str.replace(" ", "", regex=False)
    else:
        st.error("❌ 'Stock' column not found in dataset!")
        st.stop()

    # ----------------------
    # Close Price column check
    # ----------------------
    if "Close" not in df.columns:
        st.error("❌ 'Close' column not found in dataset!")
        st.stop()

    # Ensure numeric
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
    df = df.dropna(subset=["Close"])

    # ----------------------
    # Calculate SMA50 & SMA200
    # ----------------------
    df = df.sort_values(["Stock", "Date"])
    df["SMA_50"] = df.groupby("Stock")["Close"].transform(lambda x: x.rolling(50, min_periods=1).mean())
    df["SMA_200"] = df.groupby("Stock")["Close"].transform(lambda x: x.rolling(200, min_periods=1).mean())

    # ----------------------
    # Category Selection
    # ----------------------
    if "Category" in df.columns:
        category = st.selectbox("Select Category:", ["All"] + df["Category"].unique().tolist())
        if category != "All":
            df_filtered = df[df["Category"] == category]
        else:
            df_filtered = df.copy()
    else:
        df_filtered = df.copy()

    # ----------------------
    # Stock Selection
    # ----------------------
    stocks = sorted(df_filtered["Stock"].unique())
    stock = st.selectbox("Select Stock:", stocks)

    stock_df = df_filtered[df_filtered["Stock"] == stock]

    # ----------------------
    # Plotting Options
    # ----------------------
    st.subheader(f"📈 {stock} Stock Price with SMA50 & SMA200")

    chart_type = st.radio("Select Chart Type:", ["Interactive (Plotly)", "Static (Matplotlib)"])

    if chart_type == "Interactive (Plotly)":
        fig = px.line(
            stock_df,
            x="Date",
            y=["Close", "SMA_50", "SMA_200"],
            labels={"value": "Price", "variable": "Indicator"},
            title=f"{stock} Price with SMA50 & SMA200"
        )
        fig.update_layout(legend_title_text="Series", hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)

    else:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(stock_df["Date"], stock_df["Close"], label="Close", marker="o", markersize=3)
        ax.plot(stock_df["Date"], stock_df["SMA_50"], label="SMA 50", linestyle="--")
        ax.plot(stock_df["Date"], stock_df["SMA_200"], label="SMA 200", linestyle="--")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        ax.set_title(f"{stock} Price with SMA50 & SMA200")
        ax.legend()
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # ----------------------
    # Show Data & Download
    # ----------------------
    with st.expander("📄 Show Processed Data"):
        st.dataframe(stock_df.head(100))

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Cleaned Data", data=csv, file_name="nifty_cleaned.csv", mime="text/csv")

else:
    st.info("📥 Please upload a CSV file to begin.")
