import plotly.express as px
import streamlit as st 

def log_sum_PSD_scatterplot(data,threshold,color):

    f = px.scatter(data, x = "spectrum_index", y = "log_sum_PSD", 
                   color = color.replace(" ","_"),
                   hover_data = ["patient_name"], 
                  color_discrete_sequence= ['rgb(247,85,85)','rgb(0,134,255)'], 
                  opacity = 0.5)
    f.update_traces(
        marker_line = dict(color = "black",width=1))
        
    f.add_hline(y=threshold, line_dash = "dash", line_color = "white")
    return f 
    
    
def spectra_lineplot(data): 
    return px.line(data, x = "wavelength", y = "amplitude", line_group = "patient_state", color = "cell_type", 
                  color_discrete_sequence= ['rgb(0,134,255)','rgb(247,85,85)'])