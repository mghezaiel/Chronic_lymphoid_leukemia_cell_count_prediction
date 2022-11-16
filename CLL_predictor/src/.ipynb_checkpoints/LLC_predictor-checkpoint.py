import sys
sys.path.append("..")
import pandas as pd 
import os 
from app import app
from data_processing import get_log_sum_PSD
import streamlit as st 


# PATHS
DIR = os.path.dirname(os.getcwd())
DATA_DIR = os.path.join(DIR,"data")
APP_DATA_DIR = os.path.join(DIR,"app_data")


if __name__ == "__main__":
    
    # If QC is not performed
    if not "processed_data.csv" in os.listdir(DATA_DIR):
        
        # Display a spinner until QC has finished
        with st.spinner('Performing QC for the first time ...'):
            
            # Load the raw data
            data = pd.read_csv(os.path.join(DATA_DIR,"raw_data.csv"), sep =";")
       
            # Perform QC
            data = get_log_sum_PSD(data)
            
            # Save the dataframe in the data dir
            data.to_csv(os.path.join(DATA_DIR,"processed_data.csv"), sep = ";",index = False)
            
            # Notify the user on QC completion
            st.success("Done!")
        
        # Run the app
        app(data,APP_DATA_DIR)
    
    else: 
        
        # Load the processed data
        data = pd.read_csv(os.path.join(DATA_DIR,"processed_data.csv"),sep =";")
        
        # Run the app
        app(data,APP_DATA_DIR)
