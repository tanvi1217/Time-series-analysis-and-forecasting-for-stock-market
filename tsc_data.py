import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

# Load CSV
df = pd.read_csv("Quote-Equity-TCS-EQ-04-07-2025-to-04-08-2025.csv")

# Clean column names (remove spaces)
df.columns = df.columns.str.strip()

df['Date'] = pd.to_datetime(df['Date'])

# Set 'Date' as the index
df.set_index('Date', inplace=True)
df.sort_index(inplace=True)

# Plot the 'close' column (lowercase!)
plt.figure(figsize=(12, 6))
plt.plot(df['close'], label='Closing Price', color='blue')
plt.title("TCS Stock Closing Price Over Time")
plt.xlabel("Date")
plt.ylabel("Price (INR)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
#HERE I GET GRAPH

# Convert 'close' to numeric (if not already)
df['close'] = pd.to_numeric(df['close'], errors='coerce')

# Add moving averages
df['MA_5'] = df['close'].rolling(window=5).mean()
df['MA_10'] = df['close'].rolling(window=10).mean()

# Plot with moving averages
plt.figure(figsize=(12, 6))
plt.plot(df['close'], label='Closing Price', color='blue')
plt.plot(df['MA_5'], label='5-Day MA', color='green', linestyle='--')
plt.plot(df['MA_10'], label='10-Day MA', color='red', linestyle='--')
plt.title("TCS Stock Price with 5-Day and 10-Day Moving Averages")
plt.xlabel("Date")
plt.ylabel("Price (INR)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
# STEP 2: Plot with moving averages

# Convert 'VOLUME' to numeric
df['VOLUME'] = pd.to_numeric(df['VOLUME'], errors='coerce')

# Plot Closing Price and Volume in two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# Plot closing price with MAs
ax1.plot(df['close'], label='Closing Price', color='blue')
ax1.plot(df['MA_5'], label='5-Day MA', color='green', linestyle='--')
ax1.plot(df['MA_10'], label='10-Day MA', color='red', linestyle='--')
ax1.set_title("TCS Stock Price with Moving Averages")
ax1.set_ylabel("Price (INR)")
ax1.legend()
ax1.grid(True)

# Plot volume
ax2.bar(df.index, df['VOLUME'], color='gray')
ax2.set_title("Trading Volume Over Time")
ax2.set_xlabel("Date")
ax2.set_ylabel("Volume")
ax2.grid(True)

plt.tight_layout()
plt.show()
# STEP 3: Plot Closing Price and Volume in two subplots

from ta.momentum import RSIIndicator

# Calculate RSI
rsi = RSIIndicator(close=df['close'], window=14)
df['RSI'] = rsi.rsi()

# Plot RSI
plt.figure(figsize=(12, 4))
plt.plot(df['RSI'], label='RSI (14)', color='purple')
plt.axhline(70, color='red', linestyle='--', label='Overbought (70)')
plt.axhline(30, color='green', linestyle='--', label='Oversold (30)')
plt.title("Relative Strength Index (RSI) - TCS")
plt.xlabel("Date")
plt.ylabel("RSI Value")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
# STEP 4: Calculate and plot RSI

from ta.trend import MACD

# Calculate MACD
macd_indicator = MACD(close=df['close'], window_slow=26, window_fast=12, window_sign=9)
df['MACD'] = macd_indicator.macd()
df['MACD_Signal'] = macd_indicator.macd_signal()
df['MACD_Diff'] = macd_indicator.macd_diff()

# Plot MACD
plt.figure(figsize=(12, 4))
plt.plot(df['MACD'], label='MACD', color='blue')
plt.plot(df['MACD_Signal'], label='Signal Line', color='orange')
plt.bar(df.index, df['MACD_Diff'], label='MACD Histogram', color='grey')
plt.title("MACD - TCS")
plt.xlabel("Date")
plt.ylabel("MACD Value")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
# STEP 5: Calculate and plot MACD

# Prepare OHLC data
ohlc_df = df[['OPEN', 'HIGH', 'LOW', 'close', 'VOLUME']].copy()
ohlc_df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

# Convert to numeric
for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
    ohlc_df[col] = pd.to_numeric(ohlc_df[col], errors='coerce')

ohlc_df.dropna(inplace=True)

# Debug: Print shape
print("OHLC data shape:", ohlc_df.shape)
print(ohlc_df.head())

# Plot only if there's data
if not ohlc_df.empty:
    mpf.plot(ohlc_df, type='candle', volume=True, title="TCS Candlestick Chart", style='yahoo')
else:
    print("No valid rows to plot. Please check if your CSV has missing or non-numeric values.")
