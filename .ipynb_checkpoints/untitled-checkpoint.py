import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np 
from streamlit_plotly_events import plotly_events
import plotly.express as px
from scipy.stats import fisher_exact
import sys
sys.path.append("..")
from data_processing import *
from statistical_tests import *
from data_visualization import *


data = pd.read_csv("test_df.csv")


tab1,tab2,tab3,tab4 = st.tabs(["Data","Tests","How to", "QC info"])
selected_points = False
curr_data = data.copy()
patient_name = data.sample(n = 1)["patient_name"].values[0]

with tab1:  
    sidebar = st.sidebar
    
    uploaded_file = sidebar.file_uploader("Upload data")
    
    if uploaded_file:
        curr_data = load_data(uploaded_file,curr_data)
        
    threshold = sidebar.slider('Noise filtering', min_value = float(curr_data["log_sum_PSD"].median()), 
                                   max_value = float(max(curr_data["log_sum_PSD"])),
                                   step = 0.0001, value = float(curr_data["log_sum_PSD"].median()),key = "threshold")
    
    
        
    patient_name = sidebar.selectbox(
            'Select patient',
            curr_data["patient_name"].unique())
    
   

    curr_data["PSD_filtered"] = [1 if PSD>threshold else 0 for PSD in curr_data["log_sum_PSD"]]
            
    with st.container():
        st.title("Patients")
        color = st.selectbox(
            'Color spectra by:',
            ('patient state','cell type'))
        
        
        
        #sidebar.write("text")
        c1,c2 = st.columns([5,2])
        
        
        with c1: 
            f = log_sum_PSD_scatterplot(curr_data,threshold,color)
            selected_points = plotly_events(f)
    
            
        
        with c2:

            spectra_table = get_table(curr_data)
            st.table(spectra_table)
            p_values = get_fisher_exact_test_p_values(curr_data)
            Q1,median,Q3 = get_p_values_df_statistics(p_values)
            st.caption("Fisher exact test")
            st.caption(f"Q1: {Q1.round(2)}")
            st.caption(f"median: {median.round(2)}")
            st.caption(f"Q3: {Q3.round(2)}")


    with st.container():
        
        
        if selected_points:
            patient_name = curr_data[curr_data["spectrum_index"]==selected_points[0]["x"]]["patient_name"].values[0]

        st.header(f"Patient id: {patient_name}")
        c1,c2 = st.columns([5,2])
        
        patient_table,patient_data = get_patient_data(curr_data,patient_name)
        
        
        with c1: 
            f = spectra_lineplot(patient_data)
            selected_spectra = plotly_events(f)
        
        with c2:
            st.table(patient_table)
            statistic,p_val = make_fisher_exact_test(patient_table)
            if p_val is not None: 
                c2.caption("Fisher exact test")
                c2.caption(f"p value: {np.round(p_val,2)}")

with tab2: 
    st.write("how it works")
    
with tab3: 
    st.write("Details on the QC")