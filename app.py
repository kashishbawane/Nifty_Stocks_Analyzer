import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------
# Load Dataset
# ----------------------
st.title("📊 Interactive Stock Analyzer with SMA")

uploaded_file = st.file_uploader("Upload your stock dataset (CSV)", type=["csv"])

if uploaded_file is not None:
    # Read CSV
    df = pd.read_csv(uploaded_file)

    # Show raw columns
    st.subheader("Raw Data Preview")
    st.write(df.head())
    st.write("Columns in file:", df.columns.tolist())

    # ----------------------
    # Data Cleaning
    # ----------------------
    # Fix Stock column
    if "Stock" in df.columns:
        df["Stock"] = df["Stock"].astype(str).replace(" ", "", regex=True)
    
    # Fix Date column safely
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"])
    else:
        st.error("❌ No 'Date' column found in CSV.")
        st.stop()

    # Calculate SMAs
    if "Close" in df.columns:
        df["SMA_50"] = df["Close"].rolling(window=50, min_periods=1).mean()
        df["SMA_200"] = df["Close"].rolling(window=200, min_periods=1).mean()
    else:
        st.error("❌ No 'Close' column found in CSV.")
        st.stop()

    # ----------------------
    # Interactive Selection
    # ----------------------
    if "Category" in df.columns:
        category = st.selectbox("Select Category:", df["Category"].unique())
        filtered_df = df[df["Category"] == category]
    else:
        st.warning("⚠ No 'Category' column found. Showing all data.")
        filtered_df = df

    if "Stock" in filtered_df.columns:
        stock = st.selectbox("Select Stock:", filtered_df["Stock"].unique())
        stock_df = filtered_df[filtered_df["Stock"] == stock]
    else:
        st.error("❌ No 'Stock' column found in CSV.")
        st.stop()

    # ----------------------
    # Plotting
    # ----------------------
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(stock_df["Date"], stock_df["Close"], label="Close Price", marker='h', color='purple')
    ax.plot(stock_df["Date"], stock_df["SMA_50"], label="SMA 50", linestyle="--", color='blue')
    ax.plot(stock_df["Date"], stock_df["SMA_200"], label="SMA 200", linestyle="--", color='red')

    ax.set_title(f"{stock} - Price with SMA50 & SMA200")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.xticks(rotation=45)
    ax.legend()
