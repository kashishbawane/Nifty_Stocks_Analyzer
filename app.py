# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="📊 Nifty Stock Analysis Dashboard", layout="wide")
st.title("📊 Nifty Stock Analysis Dashboard with SMA50 & SMA200 + Quick Insights")

uploaded_file = st.file_uploader("Upload your Nifty Stock dataset (CSV)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("🔎 Data Preview")
    st.dataframe(df.head())

    # ---------------------- Date Column ----------------------
    if "Date" not in df.columns:
        st.error("❌ 'Date' column not found!")
        st.stop()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])

    # ---------------------- Stock Column ----------------------
    if "Stock" not in df.columns:
        st.error("❌ 'Stock' column not found!")
        st.stop()
    df["Stock"] = df["Stock"].astype(str).str.strip().str.replace(" ", "", regex=False)

    # ---------------------- Close Column ----------------------
    if "Close" not in df.columns:
        st.error("❌ 'Close' column not found!")
        st.stop()
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
    df = df.dropna(subset=["Close"])

    # ---------------------- Calculate SMA ----------------------
    df = df.sort_values(["Stock", "Date"])
    df["SMA_50"] = df.groupby("Stock")["Close"].transform(lambda x: x.rolling(50, min_periods=1).mean())
    df["SMA_200"] = df.groupby("Stock")["Close"].transform(lambda x: x.rolling(200, min_periods=1).mean())

    # ---------------------- Filters ----------------------
    if "Category" in df.columns:
        category = st.selectbox("Select Category:", ["All"] + df["Category"].unique().tolist())
        if category != "All":
            df_filtered = df[df["Category"] == category]
        else:
            df_filtered = df.copy()
    else:
        df_filtered = df.copy()

    stocks = sorted(df_filtered["Stock"].unique())
    stock = st.selectbox("Select Stock:", stocks)
    stock_df = df_filtered[df_filtered["Stock"] == stock]

    # ---------------------- Quick Insights ----------------------
    st.subheader("📌 Quick Insights")

    if not stock_df.empty:
        last_close = stock_df["Close"].iloc[-1]
        last_sma50 = stock_df["SMA_50"].iloc[-1]
        last_sma200 = stock_df["SMA_200"].iloc[-1]
        high_price = stock_df["Close"].max()
        low_price = stock_df["Close"].min()

        # Golden Cross / Death Cross
        if last_sma50 > last_sma200:
            signal = "🟢 Golden Cross (Bullish)"
        elif last_sma50 < last_sma200:
            signal = "🔴 Death Cross (Bearish)"
        else:
            signal = "⚪ Neutral (SMA50 = SMA200)"

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Last Closing Price", f"₹{last_close:.2f}")
        with col2:
            st.metric("52-Period High", f"₹{high_price:.2f}")
        with col3:
            st.metric("52-Period Low", f"₹{low_price:.2f}")

        st.markdown(f"**Trend Signal:** {signal}")

    # ---------------------- Plot ----------------------
    st.subheader(f"📈 {stock} Price Chart")

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

    # ---------------------- Data Table + Download ----------------------
    with st.expander("📄 Show Processed Data"):
        st.dataframe(stock_df.tail(100))

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Cleaned Data", data=csv, file_name="nifty_cleaned.csv", mime="text/csv")

else:
    st.info("📥 Please upload a CSV file to begin.")
