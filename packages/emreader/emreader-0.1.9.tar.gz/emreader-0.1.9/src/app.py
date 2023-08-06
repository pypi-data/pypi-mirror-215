import os

import pandas as pd
import rich
import streamlit as st

from core.base import extract_from_files
from core.util import transform_dataframe
from core.eml import extract_emails, extract_from_file
from core import store

#@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")


#@st.cache_data
def get_emails():
    rich.print("Extracting attachments from emails")
    extract_emails()

#@st.cache_data
def load_and_parse(pivot_value="Seller"):
    data = extract_from_files()
    rich.print("Running dataframe transformation...")
    rich.print(f"Using pivot value: {data}")
    transforms = transform_dataframe(data, pivot_value=pivot_value)
    rich.print(transforms[0],"rwa")
    rich.print(transforms[1],"format")
    return transforms


def handle_uploaded_file(uploads, target_dir):
    for upload in uploads:
        if upload is not None:
            #if upload.name.endswith('.zip'):
            #    with zipfile.ZipFile(upload, 'r') as zip_ref:
            #        zip_ref.extractall(target_dir)
            #else:
            #with open(os.path.join(target_dir, upload.name), "wb") as f:
            extract_from_file(upload)


def run_app():
    """
    Runs a small streamlit app to transform emails to df

    - Expects emails to be in the storage/source/emails folder.
        - These must be in .eml format
    - Automatically fetches all pdf attachments and saves to output.
     - Cleans the data for SBO prices.
    :return:
    """
    
    tab1, tab2 = st.tabs(["Upload", "Download"])
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    with tab1:
        uploaded_file = st.file_uploader("Choose a file", type=['eml'], accept_multiple_files=True)
        if uploaded_file is not None:
            handle_uploaded_file(uploaded_file, os.path.join(base_dir, "storage", "source", "emails"))
    
        # click to extract emails
        if st.button("Extract emails"):
            get_emails()
            rich.print("Done extracting emails")
            
        # list of files storage/output
        output_dir = os.path.join(base_dir, "storage", "output")
        files = os.listdir(output_dir)
        
        with st.expander("Uploaded files"):
            st.write("Files in the output folder:")
            # dataframe so we can show in table
            # add actions colum
            df = pd.DataFrame(files, columns=["Filename"])
            # add actions column
            df["actions"] = ""
            
            st.data_editor(df, column_config={
                    "actions": st.column_config.CheckboxColumn(
                        "Delete",
                        help="Select your **favorite** widgets",
                        default=False,
                    )
            })
        
    with tab2:

        st.write("App to transform emails to df")
        # inputs here for pivot value
        if st.button("Transform data"):
            option = st.selectbox(
                "Which pivot value would you like to use?", ("Seller", "Buyer")
            )
        
            df, original_df = load_and_parse(pivot_value=option)
            st.write(df)
            
            with st.expander("Original data"):
                st.write(
                    """
                    Here is the original dataframe:
                    It shows the data as it was extracted from the emails.
                    """
                )
                st.write(original_df)
        
            csv = convert_df(df)
        
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name="sob.csv",
                mime="text/csv",
            )


if __name__ == "__main__":
    run_app()
