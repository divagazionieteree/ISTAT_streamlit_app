import pandas as pd
import streamlit as st 
import matplotlib.pyplot as plt
from istatapi import discovery, retrieval

st.set_page_config(
    page_title="Home",
    layout="wide",
    page_icon="👋",
)

st.title('Istat')

st.write("Uploading Employment rate  - monthly data")

ds = discovery.DataSet(dataflow_identifier="150_872") 
trade_df = retrieval.get_data(ds)

st.write("Employment rate  - monthly data OK")

if ds not in st.session_state:
    st.session_state.empl_rate_monthly = ds
    st.session_state.empl_rate_monthly_trade = trade_df

st.write("Uploading Resident population on 1st January")

# initialize the dataset and get its dimensions
ds1 = discovery.DataSet(dataflow_identifier="22_289")

if ds1 not in st.session_state:
    st.session_state.resident_population = ds1

st.write("Resident population on 1st January OK")


