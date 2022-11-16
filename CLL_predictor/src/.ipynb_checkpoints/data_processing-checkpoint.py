import sys 
import streamlit as st 
import pandas as pd 
from scipy.signal import periodogram
import numpy as np 
from collections import Counter 
from datetime import datetime 

def get_log_CSD(data,threshold = 2,fs = 10): 
    """Computes log cumulated power spectral density 
    above a defined threshold for each spectra
    
    args: 
        data: Dataframe of the raw data (pd.DataFrame)
        threshold: Threshold value for the cumulated spectral density (CSD) (Hz)
        fs: sampling frequency (Hz)
        
    return: 
        data: Dataframe with log_CSD and spectrum_index columns (pd.DataFrame)
        
    """
    
    log_CSD = []
    for ids,signal in enumerate(range(data.shape[0])):
        signal = data.filter([col for col in data.columns if "lambda" in col],axis = 1).values[signal,:]
        f, Pxx_den = periodogram(signal, fs)
        PSD_freq = [freq for freq in zip(f,Pxx_den)]
        PSD_signal = [freq[1] for freq in PSD_freq if freq[0]<=threshold]

        log_CSD.append(np.log(sum(PSD_signal)))
        
    data["log_CSD"] = log_CSD
    data["spectrum_index"] = data.index 
    return data 



@st.cache
def get_table(data):
    """Computes table of cell counts before and after filtering 
    on cumulated spectral density (CSD) 
    
        args:
            data: Dataframe of the raw data (pd.DataFrame)

        returns:
            spectra_table: Cell count table (pd.DataFrame)
    
    """
    before = data.groupby(["cell_type","cell_name"]).count()["patient_name"]
    after = data[data["CSD_filtered"]==1].groupby(["cell_type","cell_name"]).count()["patient_name"]
    spectra_table = pd.concat([before,after],axis = 1)
    spectra_table.columns = ["Before","After"]
    spectra_table = spectra_table.applymap(lambda x: 1 if x>0 else 0).reset_index().groupby("cell_type").sum()
    return spectra_table.fillna(int(0))


@st.cache 
def get_patient_data(data,patient_name): 
    """Get patient data from the raw data giving patient name.
    
        args:
            data: DataFrame of the raw data (pd.DataFrame)
            patient_name: Patient name (str)

        returns:
            patient_table: Cell count table of the target patient (pd.DataFrame)
            patient_data: Melted dataFrame of the raw data (pd.DataFrame)

    """
    patient_data = data[data["patient_name"]==patient_name]
    patient_table = get_table(patient_data)
    patient_data = pd.melt(patient_data, id_vars = ["spectrum_index","cell_type","cell_name","patient_state"],
                           value_vars = [col for col in patient_data.columns if "lambda" in col])
    patient_data["variable"] = patient_data["variable"].apply(lambda x: x.replace("lambda_",""))
    patient_data = patient_data.rename(columns = {"variable":"wavelength","value":"amplitude"})    
    return patient_table,patient_data 

@st.cache
def get_cells_statistics(patient_table):
    """Calculates b cell fraction, tnk cell fr&action and b/tnk ratio
    
        args: 
            patient_table: Cell count table of the target patient
        return: 
            b_cells_fraction: (float)
            tnk_cells_fraction: (float)
            b_tnk_ratio: (float)
    
    """
    counts = patient_table["After"]
    b_cells_fraction = np.round(counts[counts.index=="B"].values[0]/sum(counts.values),2) if "B" in counts else 0 
    tnk_cells_fraction = np.round(counts[counts.index == "TNK"].values[0]/sum(counts.values),2) if "TNK" in counts else 0 
    b_tnk_ratio = np.round(b_cells_fraction/tnk_cells_fraction,2) if tnk_cells_fraction!=0 else 0
    return b_cells_fraction,tnk_cells_fraction,b_tnk_ratio

def get_time():
     """Get date and time
         returns: 
             date and time in format %d-%m-%Y_%H_%M_%S
     """
     return datetime.today().strftime("%d-%m-%Y_%H_%M_%S")
        
        