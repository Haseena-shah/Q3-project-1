import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout="wide")

# Custom CSS
st.markdown(
    """
    <style>
    .stapp{
        background-color: black;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("Data Sweeper app by Hassi Shah")
st.write("This app is used to clean the data and remove unwanted columns from the data.")

# File upload
uploaded_files = st.file_uploader("Upload your file (accepts csv or excel file):", type=['csv', 'xlsx'], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        # Load file based on extension
        if file_ext == '.csv':
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # Preview the dataframe
        st.write("🔎 Preview the head of the data frame")
        st.dataframe(df.head())

        # Data cleaning options
        st.subheader("⚙️ Data cleaning options")
        if st.checkbox(f"Clean data for {file.name}"):
            st.write("🔥 Remove unwanted columns")
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from the file: {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates removed")

            with col2:
                if st.button(f"Fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing values have been filled")
                
            st.subheader("Select columns to keep")     
            columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
            df = df[columns]

            # Data visualization
            st.subheader("📊 Data visualization")
            if st.checkbox(f"Show data visualization for {file.name}"):
                st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

            # Conversion options
            st.subheader("📤 Data conversion options")
            conversation_type = st.radio(f"Convert {file.name} to", ["csv", "Excel"], key=file.name) 
            if st.button(f"Convert {file.name}"):
                buffer = BytesIO()
                if conversation_type == "csv":
                    df.to_csv(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"
                elif conversation_type == "Excel":
                    df.to_excel(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                buffer.seek(0)

                st.download_button(
                    label=f"Click here to download {file_name} as converted {conversation_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type,
                )

st.success("✅ All tasks completed successfully")

