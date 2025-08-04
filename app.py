import streamlit as st
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt

# Title
st.title("📈 TCS Candlestick Chart")

# Upload CSV
uploaded_file = st.file_uploader("Upload your TCS stock CSV file", type=["csv"])
if uploaded_file:
    try:
        # Read CSV
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip().str.lower()  # clean column names

        # Show shape before cleaning
        st.write("📊 Original shape:", df.shape)

        # Convert 'date' to datetime
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

        # Clean numeric columns
        numeric_cols = ['open', 'high', 'low', 'close', 'volume']
        for col in numeric_cols:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(',', '', regex=False)
                .str.replace('-', '', regex=False)
                .str.replace('—', '', regex=False)
            )
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # Drop NaNs
        df.dropna(subset=numeric_cols, inplace=True)
        st.write("✅ After cleaning:", df.shape)

        if df.empty:
            st.error("🚫 No valid data to plot.")
        else:
            df.set_index('date', inplace=True)
            df.sort_index(inplace=True)

            # Plot
            st.write("📉 Candlestick Chart:")
            fig, axlist = mpf.plot(
                df,
                type='candle',
                volume=True,
                style='yahoo',
                mav=(5, 10),
                returnfig=True
            )
            st.pyplot(fig)

    except Exception as e:
        st.error(f"⚠️ Error processing file: {e}")
else:
    st.info("⬆️ Upload a CSV file to see the candlestick chart.")
