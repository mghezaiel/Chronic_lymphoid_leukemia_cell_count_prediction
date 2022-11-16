import pandas as pd 
from scipy.stats import fisher_exact
import streamlit as st 
import numpy as np 
from data_processing import get_table 

def make_fisher_exact_test(table): 
    """ Computes Fisher's exact test 
    args: 
        table: cell count table (pd.DataFrame)
    return: 
        tuple: tuple of statistic and p value (tuple)
    
    """
    return fisher_exact(table) if table.shape==(2,2) else (None,None)

@st.cache
def get_fisher_exact_test_p_values(data):
    """ Iterates through the dataframe and compute Fisher's exact tests
    args: 
        data: dataframe (pd.DataFrame)
    return: 
        p_values: dataframe of p_values (pd.DataFrame)
    """
    p_values = [make_fisher_exact_test(get_table(data[data["patient_name"]==patient_name]))
                for patient_name in np.unique(data["patient_name"])]
    p_values = pd.DataFrame(p_values,columns = ["statistic","p_value"])
    p_values["patient_name"] = data["patient_name"].unique()
    return p_values 

def get_p_values_df_statistics(df):
    """ Get quantiles of the p values df 
    args: 
        df: dataframe of p values (pd.DataFrame)
    return: 
        Q1,median,Q2: quantiles of p_values (float)
    
    """
    df = df.dropna()
    Q1 = np.quantile(df["p_value"],0.25).round(2)
    median = np.median(df["p_value"]).round(2)
    Q3 = np.quantile(df["p_value"],0.75).round(2)
    return Q1,median,Q3

    
