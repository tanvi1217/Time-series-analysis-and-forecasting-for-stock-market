import streamlit as st
import pandas as pd

st.title("📊 Stock Data Viewer")

# Load Excel data
@st.cache_data
def load_stock_data():
    return pd.read_excel("stock_data_database.xlsx", sheet_name=None)

# Load all company sheets
stock_data = load_stock_data()

# Sidebar: select company sheet
selected_company = st.sidebar.selectbox("🏢 Select Company", list(stock_data.keys()))

# Get the selected DataFrame
df = stock_data[selected_company]

st.subheader(f"📈 Data for {selected_company}")

# Search box
search_term = st.text_input("🔍 Search in data (e.g., date or value):")

# Filtered display
if search_term:
    filtered_df = df[df.astype(str).apply(lambda row: row.str.contains(search_term, case=False)).any(axis=1)]
    st.write(f"🔎 Showing results for **{search_term}**:")
    st.dataframe(filtered_df)
else:
    st.dataframe(df)

# Show stats
st.markdown("### ℹ️ Summary Info")
st.write(df.describe())

st.markdown("### 🧮 Data Shape")
st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
