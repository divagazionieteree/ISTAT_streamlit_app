import pandas as pd
import streamlit as st 
import matplotlib.pyplot as plt
from istatapi import discovery, retrieval


st.set_page_config(
    page_title="150_872 - Employment rate  - monthly data",
    layout="wide",
    page_icon="👋",
)

st.title('150_872 - Employment rate  - monthly data')

values = st.slider("Select a range of values", 2004, 2024, (2004, 2024))

ds = st.session_state.empl_rate_monthly   #Employment rate  - monthly data
trade_df = st.session_state.empl_rate_monthly_trade

dimension = "CLASSE_ETA" #use "dimension" column from above
options_check = st.selectbox("Variabile", ds.get_dimension_values(dimension)["values_ids"])

#freq = "M" #monthly frequency
#tipo_dato = ["EMP_R"] #imports and exports seasonally adjusted data

#ds.set_filters(freq = freq, tipo_dato = tipo_dato)

#trade_df = retrieval.get_data(ds)

trade_df_1 = trade_df[trade_df["CLASSE_ETA"] == options_check]

#replace the "TIPO_DATO" column values with more meaningful labels
trade_df_1["SESSO"] = trade_df_1["SESSO"].replace({1: "Male", 2: "Female", 9: "Total"})

# Plot the data
after_year = trade_df_1["TIME_PERIOD"] >= str(values[0])
previous_year = trade_df_1["TIME_PERIOD"] <= str(values[1]) 
is_MALE = trade_df_1["SESSO"] == "Male"
is_FEMALE = trade_df_1["SESSO"] == "Female"
is_TOTAL = trade_df_1["SESSO"] == "Total"

male = trade_df_1[is_MALE & after_year & previous_year].rename(columns={"OBS_VALUE": "Male"})
female = trade_df_1[is_FEMALE & after_year & previous_year].rename(columns={"OBS_VALUE": "Female"})
total = trade_df_1[is_TOTAL & after_year & previous_year].rename(columns={"OBS_VALUE": "Total"})

fig1, ax1 = plt.subplots(figsize=(20,8))
ax1.set_xlabel('Year')
ax1.set_ylabel('%')
ax1.set_title('Employment rate  - monthly data')

colors = ['#30a2da', '#fc4f30', '#e5ae38', '#6d904f', '#8b8b8b']

ax1.plot(
    "TIME_PERIOD",
    "Male",
    data=male,
    color = colors[0]
)
ax1.plot(
    "TIME_PERIOD",
    "Female",
    data=female,
    color = colors[1]
)
ax1.plot(
    "TIME_PERIOD",
    "Total",
    data=total,
    color = colors[2]
)

ax1.legend()
st.pyplot(fig1)