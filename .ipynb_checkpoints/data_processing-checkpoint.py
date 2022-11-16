import sys 
import streamlit as st 
import pandas as pd 
from scipy.signal import periodogram
import numpy as np 

def get_log_sum_PSD(data): 
    log_sum_PSD = []
    for ids,signal in enumerate(range(data.shape[0])):
        signal = data.filter([col for col in data.columns if "lambda" in col],axis = 1).values[signal,:]
        fs = 10 
        f, Pxx_den = periodogram(signal, fs)
        PSD_freq = [freq for freq in zip(f,Pxx_den)]
        PSD_signal = [freq[1] for freq in PSD_freq if freq[0]<=2]

        log_sum_PSD.append(np.log(sum(PSD_signal)))
        
    data["log_sum_PSD"] = log_sum_PSD
    data["spectrum_index"] = data.index 
    return data 

@st.cache
def get_table(data,ratio = False):
    before = data.groupby("cell_type").count()["patient_name"]
    after = data[data["PSD_filtered"]==1].groupby("cell_type").count()["patient_name"]
    spectra_table = pd.concat([before,after],axis = 1)
    spectra_table.columns = ["Before","After"]
    # Add lacking cells to table
    
    if ratio:
        before_ratio = spectra_table["Before"][0]/spectra_table["Before"].sum()
        after_ratio = spectra_table["Before"][0]/spectra_table["Before"].sum()
        row = pd.DataFrame({"Before":before_ratio,"After":after_ratio}, 
                           columns = ["Before","After"],index = ["B cell fraction"])
        
        return spectra_table.append({"Before":before_ratio,"After":after_ratio}, ignore_index = True)
    
    return spectra_table.fillna(int(0))


@st.cache 
def get_patient_data(data,patient_name): 
    patient_data = data[data["patient_name"]==patient_name]
    patient_table = get_table(patient_data,ratio = False)
    patient_data = pd.melt(patient_data, id_vars = ["spectrum_index","cell_type","cell_name","patient_state"],
                           value_vars = [col for col in patient_data.columns if "lambda" in col])
    patient_data["variable"] = patient_data["variable"].apply(lambda x: x.replace("lambda_",""))
    patient_data = patient_data.rename(columns = {"variable":"wavelength","value":"amplitude"})    
    return patient_table,patient_data 

def load_data(uploaded_data,data):
    try:
        uploaded_data = pd.read_csv(uploaded_data)
    except: 
        raise Exception("Incorrect file type")
    uploaded_data = get_log_sum_PSD(uploaded_data)
    return add_data_to_df(data,uploaded_data)
    
    
    
    

        