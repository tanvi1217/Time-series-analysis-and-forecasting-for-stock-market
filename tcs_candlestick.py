import pandas as pd
import mplfinance as mpf

def load_and_clean_data(csv_file):
    """
    Load CSV file and clean data for candlestick plotting.
    """
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"🚫 File not found: {csv_file}")
        return None

    # Standardize column names to lowercase without spaces
    df.columns = df.columns.str.strip().str.lower()

    print(f"📊 Original shape: {df.shape}")

    # Convert 'date' to datetime, coerce errors to NaT
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Define numeric columns expected
    numeric_cols = ['open', 'high', 'low', 'close', 'volume']

    # Clean numeric columns: remove commas, em dashes, strip spaces
    for col in numeric_cols:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(',', '', regex=False)
                .str.replace('—', '', regex=False)
                .str.strip()
            )
            df[col] = pd.to_numeric(df[col], errors='coerce')
        else:
            print(f"🚫 Missing expected column: {col}")
            return None

    # Drop rows where numeric data or date is missing/invalid
    df.dropna(subset=numeric_cols + ['date'], inplace=True)

    print(f"✅ After cleaning: {df.shape}")

    if df.empty:
        print("🚫 No valid data to plot. Please check your CSV content.")
        return None

    # Set date as index and sort by date ascending
    df.set_index('date', inplace=True)
    df.sort_index(inplace=True)

    return df

def plot_candlestick(df, title="Candlestick Chart"):
    """
    Plot candlestick chart using mplfinance with volume and moving averages.
    """
    mpf.plot(
        df,
        type='candle',
        volume=True,
        title=title,
        style='yahoo',
        mav=(5, 10),
        tight_layout=True,
        show_nontrading=False,
        figsize=(12, 8)
    )

def main():
    csv_file = "Quote-Equity-TCS-EQ-04-07-2025-to-04-08-2025.csv"

    df = load_and_clean_data(csv_file)
    if df is not None:
        plot_candlestick(df, title="TCS Candlestick Chart")

if __name__ == "__main__":
    main()
