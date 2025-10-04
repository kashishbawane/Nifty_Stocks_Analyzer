import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load your dataset (replace with your path or data source)
df = pd.read_csv("Stocks_2025.csv")

# Data cleaning & preprocessing
df["Date"] = pd.to_datetime(df["Date"])
df["Stock"] = df["Stock"].replace(" ", "", regex=True)

# Calculate SMA 50 & SMA 200
df["SMA_50"] = df["Close"].rolling(window=50, min_periods=1).mean()
df["SMA_200"] = df["Close"].rolling(window=200, min_periods=1).mean()

# Streamlit App
st.title("📈 Interactive Stock Analysis with SMA")

# Category selection
category = st.selectbox("Select Category:", df["Category"].unique())

# Filter by category
filtered_df = df[df["Category"] == category]

# Stock selection
stock = st.selectbox("Select Stock:", filtered_df["Stock"].unique())

# Filter by stock
stock_df = filtered_df[filtered_df["Stock"] == stock]

# Plotting
fig, ax = plt.subplots(figsize=(12,6))
ax.plot(stock_df["Date"], stock_df["Close"], label="Close Price", marker='h', color='purple')
ax.plot(stock_df["Date"], stock_df["SMA_50"], label="SMA 50", linestyle="--", color='blue')
ax.plot(stock_df["Date"], stock_df["SMA_200"], label="SMA 200", linestyle="--", color='red')

ax.set_title(f"{stock} - Price with SMA50 & SMA200")
ax.set_xlabel("Date")
ax.set_ylabel("Price")
plt.xticks(rotation=45)
ax.legend()

st.pyplot(fig)
