import pandas as pd
import streamlit as st 
import matplotlib.pyplot as plt
import numpy as np
from istatapi import discovery, retrieval
import seaborn as sns

st.set_page_config(
    page_title="22_289 Resident population  on 1st January",
    layout="wide",
    page_icon="👋",
)

ds = st.session_state.resident_population

dimension = "SESSO" #use "dimension" column from above
records = ds.get_dimension_values(dimension).to_dict("records")
options_check_sesso = st.selectbox("Sesso", options=records, format_func=lambda record: f'{record["values_description"]}')

dimension = "STACIVX" #use "dimension" column from above
records = ds.get_dimension_values(dimension).to_dict("records")
options_check_marital = st.selectbox("Marital Status", options=records, format_func= lambda record: f'{record["values_description"]}')

freq = "A" #Annual frequency
itter107 = 'IT' #Italy
stacivx = options_check_marital["values_ids"] #total marital status
sesso = options_check_sesso["values_ids"] #total

ds.set_filters(freq = freq, itter107 = itter107, stacivx = stacivx, sesso = sesso)

residents_df = retrieval.get_data(ds)

def tweak_residents_df(residents_df):
    residents_df = residents_df.query('ETA != "TOTAL"').copy()
    
    residents_df = residents_df.rename(columns={"TIME_PERIOD": "year"})
    residents_df['year'] = pd.to_datetime(residents_df['year'], format='%Y')
    residents_df['ETA'] = residents_df['ETA'].astype(str).str.replace('Y', '').str.replace('_GE100', '100').astype(int)
    residents_df['ETA_bin'] = pd.cut(residents_df['ETA'], bins= [0, 25, 45, 65, np.inf], labels=['0-25', '25-45', '45-65', '65+'])
    return (residents_df.groupby(['year', 'ETA_bin']).sum().reset_index())

residents_df2 = tweak_residents_df(residents_df)

fig1, ax1 = plt.subplots(figsize=(20,8))
ax1.set_xlabel('Year')
ax1.set_ylabel('OBS_VALUE')
ax1.set_title('Resident population  on 1st January')

# Plot the data
sns.lineplot(data=residents_df2, x="year", y="OBS_VALUE", hue="ETA_bin", marker = 'X')
ax1.ticklabel_format(style='plain', axis='y')

ax1.legend()
st.pyplot(fig1)