import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np 
from streamlit_plotly_events import plotly_events
import plotly.express as px
from scipy.stats import fisher_exact
from data_processing import *
from statistical_tests import *
from data_visualization import *
from PIL import Image



def app(data,APP_DATA_DIR):
    
    # App logo
    logo = Image.open(os.path.join(APP_DATA_DIR,"app_logo.png"))
    
    # Tabs
    tab1,tab2,tab3= st.tabs(["Data","How it works", "QC details"])
    
    # On click events
    selected_points = False
    
    # Copy of the input data 
    curr_data = data.copy()
    
    # Initialize patient_name for the lower panel
    patient_name = data.sample(n = 1)["patient_name"].values[0]
    
    # Data tab
    with tab1:  
        
        # Sidebar
        sidebar = st.sidebar
        
        # Logo in the sidebar
        sidebar.image(logo)

        # Slider for the log CSD threshold
        threshold = sidebar.slider('Filter on log CSD', min_value = float(curr_data["log_CSD"].median()), 
                                       max_value = float(max(curr_data["log_CSD"])),
                                       step = 0.0001, value = float(curr_data["log_CSD"].median()),key = "threshold")

        # Select box for the selected patient
        patient_name = sidebar.selectbox(
                'Select patient',
                curr_data["patient_name"].unique(),index = 18)

        # Label spectra according to the threshold
        curr_data["CSD_filtered"] = [1 if PSD>threshold else 0 for PSD in curr_data["log_CSD"]]

        # Download button in the sidebar to download processed data
        sidebar.download_button(
            label="Download data",
            data=curr_data.set_index(
            ["spectrum_index","patient_name"],drop = True).to_csv(index = False).encode("utf-8"),
            file_name=f'processed_data_{get_time()}.csv',
            mime='text/csv',
        )

        # Upper panel
        with st.container():
            
            # Title
            st.title("Patients")
            
            # Select box to color the CSD scatterplot
            color = st.selectbox(
                'Color spectra by:',
                ('patient state','cell type'))

            # Divides the upper panel into CSD scatterplot and cell counts table
            c1,c2 = st.columns([5,2])
            
            # CSD scatterplot
            with c1: 
                
                # Plots the figure
                f = log_CSD_scatterplot(curr_data,threshold,color)
                
                # On click patient selection
                selected_points = plotly_events(f)
                
            # Cell count table
            with c2:
                
                # Computes the cell count table
                spectra_table = get_table(curr_data)
                
                # Displays the table
                st.table(spectra_table)
                
                # Computes fisher exact test p values
                p_values = get_fisher_exact_test_p_values(curr_data)
                
                # Computes quantiles for the p values distribution
                Q1,median,Q3 = get_p_values_df_statistics(p_values)
                
                # Displays the quantiles
                st.markdown("**Fisher exact test**")
                st.caption(f"Q1: {Q1.round(3)}")
                st.caption(f"median: {median.round(3)}")
                st.caption(f"Q3: {Q3.round(3)}")

        # Lower panel
        with st.container():
            
            # Filter the dataframe to the selected patient (scatterplot click or select box)
            # Else use the initialized patient name
            
            if selected_points:
                patient_name = curr_data[curr_data["spectrum_index"]==selected_points[0]["x"]]["patient_name"].values[0]
            
            # Display patient name
            st.header(f"Patient id: {patient_name}")
            
            # Get patient data and cell count table
            patient_table,patient_data = get_patient_data(curr_data,patient_name)
            
            # Download processed patient data 
            sidebar.download_button(
                label="Download patient data",
                data=curr_data[curr_data["patient_name"]==patient_name].set_index(
                    ["cell_name","spectre"],drop = True).to_csv(index = True).encode("utf-8"),
                file_name=f'processed_data_{patient_name}_{get_time()}.csv',
                mime='text/csv',
            )
        
            # Divide the lower panel into Raman spectra plot and cell count table
            c1,c2 = st.columns([5,2])
            
            # Raman spectra plot 
            with c1: 
        
                # Plot Raman spectra for the target patient
                f = spectra_lineplot(patient_data)
                
                # On click line selection
                selected_lines = plotly_events(f)
                
            # Display the cell count 
            with c2:
                
                # Plot patient data
                st.table(patient_table)
                
                # Computes the fisher exact test p value
                statistic,p_val = make_fisher_exact_test(patient_table)
                
                # p value cannot be computed for patient with null b/tnk ratio
                if p_val is not None: 
                    st.markdown("**Fisher exact test**")
                    st.caption(f"p value: {np.round(p_val,2)}")
                    st.caption(" ")
                    
            # Computes cell fractions
            cells_statistics = get_cells_statistics(patient_table)
            
            # Displays the cells fractions
            c2.markdown("**Fractions**")
            c2.caption(f"B cells: {cells_statistics[0]} ")
            c2.caption(f"TNK cells: {cells_statistics[1]} ")
            c2.caption(f"B/TNK ratio {cells_statistics[2]} ")

    # How it works tab
    with tab2: 
        
        # Read the file from the app_data dir then displays it
        with open(os.path.join(APP_DATA_DIR,"how_it_works.txt"),"r") as f:
            
            # Render using markdown format
            st.markdown(f.read())

    # QC Details tab
    with tab3:
        
        # Tab title
        st.markdown("# QC details")
        
        # Divides the page into text and figure areas
        c1,c2 = st.columns([1,1])
        
        # Read the file from the app_data dir 
        with open(os.path.join(APP_DATA_DIR,"QC_details_1.txt"),"r") as f:
            
            # Render using markdown format 
            c1.markdown(f.read())
        
        # Read the file from the app_data dir 
        with open(os.path.join(APP_DATA_DIR,"QC_details_2.txt"),"r") as f:
            
            # Render using markdown format 
            c1.markdown(f.read())
        
        # Load periodogram figure from the app_data dir
        periodogram = Image.open(os.path.join(APP_DATA_DIR,"periodogram.png"))
        
        # Displays the figure 
        c2.image(periodogram)