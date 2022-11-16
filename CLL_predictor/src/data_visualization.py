import plotly.express as px
import streamlit as st 

def log_CSD_scatterplot(data,threshold,color):
    """ Plots the CSD scatterplot
    
        args: 
            data: Dataframe (pd.DataFrame)
            threshold: log CSD threshold (float)
            color: scatterplot color label (str)
            
        return: 
            f: figure (plotly figure)
    """
    f = px.scatter(data, x = "spectrum_index", y = "log_CSD", 
                   color = color.replace(" ","_"),
                   hover_data = ["patient_name"], 
                  color_discrete_sequence= ['rgb(247,85,85)','rgb(0,134,255)'], 
                  opacity = 0.5,
                  title = "Cumulated spectral density (CSD)", 
                  labels = {"spectrum_index":"spectrum index", 
                           "log_CSD":"log CSD"})
    f.update_traces(
        marker_line = dict(color = "black",width=1))
        
    f.add_hline(y=threshold, line_dash = "dash", line_color = "white")
    return f 
    
    
def spectra_lineplot(data): 
    """ Plots the Raman spectra lineplot
    
        args: 
            data: Dataframe (pd.DataFrame)
            
        return:
            f: figure (plotly figure)
            
    """
    return px.line(data, x = "wavelength", y = "amplitude", line_group = "patient_state", color = "cell_type", 
                  color_discrete_sequence= ['rgb(247,85,85)','rgb(0,134,255)'], 
                  title = "Raman spectra")

