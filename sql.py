import streamlit as st
import pandas as pd
import sqlite3
import tempfile
import os

# Streamlit app title
st.title("CSV to SQLite Converter")

# Upload CSV file
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    # Load the CSV data into a pandas DataFrame
    df = pd.read_csv(uploaded_file, dtype=str)  # Load all columns as strings to preserve formatting
    st.write("Preview of uploaded data:")
    st.dataframe(df.head())

    # Create a temporary file to save the SQLite database with delete=False
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp_file:
        db_file_path = tmp_file.name

    try:
        # Save the DataFrame to an SQLite database file
        with sqlite3.connect(db_file_path) as conn:
            df.to_sql("data_table", conn, if_exists="replace", index=False)

        # Read the file into memory to avoid holding a file handle
        with open(db_file_path, "rb") as f:
            file_data = f.read()

        # Provide a download button for the SQLite file data
        st.download_button(
            label="Download SQLite Database",
            data=file_data,
            file_name="database.db",
            mime="application/octet-stream"
        )

        st.success("SQLite database has been created and is ready for download!")
    finally:
        # Clean up the temp file after reading it into memory
        if os.path.exists(db_file_path):
            os.remove(db_file_path)
