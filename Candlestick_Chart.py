import streamlit as st
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt

st.title("📈 Candlestick Chart Viewer")

# Upload CSV file
uploaded_file = st.file_uploader("Upload a stock CSV file", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip().str.lower()  # normalize column names

        # Convert date
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

        # Drop rows with missing values
        df.dropna(subset=numeric_cols + ['date'], inplace=True)

        # Prepare for mplfinance
        df.set_index('date', inplace=True)
        df.sort_index(inplace=True)

        st.success(f"✅ Loaded {len(df)} records.")

        # Display candlestick chart
        st.subheader("📉 Candlestick Chart")
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
        st.error(f"⚠️ Error loading or plotting the file: {e}")

else:
    st.info("⬆️ Upload a CSV file to display the candlestick chart.")
