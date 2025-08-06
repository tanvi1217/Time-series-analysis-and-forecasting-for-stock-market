import streamlit as st
import pandas as pd

# Page title
st.title("📊 Stock Data Viewer")

# Load data from Excel (make sure 'stock_data_database.xlsx' is in your root folder)
@st.cache_data
def load_stock_data():
    return pd.read_excel("stock_data_database.xlsx", sheet_name=None)

# Load all sheets
stock_data = load_stock_data()

# Sidebar for sheet (company) selection
selected_company = st.sidebar.selectbox("📁 Select Company", list(stock_data.keys()))

# Display selected company data
df = stock_data[selected_company]

st.subheader(f"📈 Data for {selected_company}")
st.dataframe(df)

# Show basic info
st.markdown("### ℹ️ Summary Info")
st.write(df.describe())

st.markdown("### 🧮 Data Shape")
st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
