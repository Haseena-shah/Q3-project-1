import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title= "data sweeper",layout="wide")

#custom css
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
#title and discription
st.title("Data Sweeper app by Hassi shah")
st.write("This app is used to clean the data and remove the unwanted columns from the data")

#file upload
uploaded_file = (st.file_uploader("upload your file (acept csv or excel file):",type=['csv','xlsx'], accept_multiple_files=True))

if uploaded_file:
    for file in uploaded_file:
        file_ext = os.path.splitext(file.name)[-1].lower()
        if file_ext == '.csv':
           df = pd.read_csv("file_path.csv")
        elif file_ext == ".xlsx":
            df = pd.read_excel('file_path.xlsx')
        else: 
         st.error(f"unsupported file type: {file_ext}")
        continue

    #files details
    st.write("🔎previwe the head of data frame")
    st.dataframe(df.head())

    #data cleaning options
    st.subheader("⚙️ data cleaning options")  
    if st.checkbox(f"clean data for {file.name}"):
        st.write("🔥 Remove the unwanted columns")
        col1, col2 = st.columns(2)

        with col1:
           if st.button(f"Remove duplicates from the file :{file.name}"):
               df.drop_duplicates(inplace=True)
               st.write("✅ duplicates removed")

        with col2:
            if st.button(f"fill missing values for {file.name}"):
                numeric_cols = df.select_dtypes(include=['number']).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.write("✅ missing values have been filled")
                 
        st.subheader  ("select columns to keep")     
        columns = st.multiselect (f"choose columns for {file.name}", df.columns, defult=df.columns)
        df = df[columns]

        #data visualization
        st.subheader("📊 data visualization")
        if st.checkbox("show data visualization for {file.name}"):
            st.bar_chart (df.select_dtypes (include="number").icol [:, :2] )
            
            #conversion options
            
            st.subheader("📤 data conversion options")
            conversation_type = st.radio (f"convert {file.name} to", ["csv", "Excel"], key=file.name) 
            if st.button (f"convert {file.name}"):
                buffer= BytesIO()
                if conversation_type == "csv":
                    df.to.csv(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"
                elif conversation_type == "Excel":
                    df.to_excel(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                buffer.seek(0)

                st.download_button(
                    label=f"click here to download {file_name} as converted {conversation_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type,
                )

st.success("✅ All tasks completed successfully")                
               
