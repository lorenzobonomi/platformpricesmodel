## Modules for project
# Standard modules
from json import load
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_ace import st_ace
from matplotlib import pyplot as plt
import seaborn as sns
import sqlite3 as sql
import altair as alt

# Ad-hoc project modules
import price as pr
import simulation as sm
from parameters import initial_riders_ratio, toledo_population,  saturation_riders, saturation_drivers

## App

# Streamlit layout main parameters
#st.set_page_config(layout = 'wide')
st.title('Price simulator for ride sharing platform in Toledo, Ohio.')
st.subheader('')

# Steramlit sidebar for car data entry and paramters for simulation
with st.sidebar:

    # Form for car data entry
    with st.form('myform_car'):

        option_acquisition = st.selectbox('Include new riders and drivers acquisition?', ('No', 'Yes'), index = 0)
        total_poulation = st.number_input('Total Toledo population', key = 'population', value = toledo_population)
        start_drivers = st.number_input('Initial drivers', key = 'start_drivers', value = 100)
        
        n_months = st.number_input('Number of months for simulation', key = 'n_months', value = 12)
        n_months_to_saturate_market = st.number_input('Number of months for market saturation', key = 'n_months', value = 24)
        start_wage = st.number_input('Starting wage for driver in $', key = 'start_wage', value = 19)
        start_price = st.number_input('Starting price for rider in $', key = 'start_price', value = 25)
        start_match_rate = st.number_input('Starting match rate', key = 'start_match_rate', value = 0.6)
        cac_driver = st.number_input('CAC for driver acquisition in $', key = 'cac_driver', value = 500)
        churn_rate_driver = st.number_input('Churn rate for driver', key = 'start_price', value = 0.2)
        rides_month_driver = st.number_input('Rides for driver for month', key = 'rides_month_driver', value = 100)
        cac_rider = st.number_input('CAC for rider acquisition in $', key = 'cac_driver', value = 10)
        churn_rate_rider_success = st.number_input('Churn rate for rider with success match', key = 'churn_rate_rider_sucess', value = 0.1)
        churn_rate_rider_failed = st.number_input('Churn rate for rider with failed match', key = 'churn_rate_rider_failed', value = 0.33)
        rides_month_rider = st.number_input('Rides for rider for month', key = 'rides_month_rider', value = 1)
        n_simulations = st.number_input('Number of simulations', key = 'n_simulations', value = 50)   
     
    
        f1, f2 = st.columns((1, 1))
        with f1:
            if st.form_submit_button('Launch Simulation'):
                load_data = 2
     

    #shape = st.slider('Distribution shape parameter', 0.0, 10.0, 1.0, key = 'shape')

# Steramlit simulation dashboard
x, y, drivers = sm.simulation_acquisition_users(start_drivers, saturation_drivers, n_months_to_saturate_market)
x, y, riders = sm.simulation_acquisition_users(start_drivers * initial_riders_ratio, saturation_riders, n_months_to_saturate_market)

st.subheader('Simulation of match rate given profit for ride')
test_profits_sm, test_match_rates_sm = sm.simulation_match_rate(0.1, 5.9, n_simulations)

fig, ax = plt.subplots() 
ax = plt.plot(test_profits_sm, test_match_rates_sm, 'red')
st.write(fig)

st.subheader('Calculation of net revenue for 12 months period with simulated match rates')
net_revenue, costs, final_drivers, final_riders = pr.calculate_net_revenue(option_acquisition, drivers[0:n_months+1], riders[0:n_months+1], cac_driver, cac_rider, start_drivers, initial_riders_ratio, test_profits_sm, test_match_rates_sm, rides_month_rider, rides_month_driver, churn_rate_driver, churn_rate_rider_success, churn_rate_rider_failed)

results_df = pd.DataFrame(list(zip(net_revenue, costs, final_drivers, final_riders, test_profits_sm, test_match_rates_sm)),
               columns =['Net Revenue', 'Costs', 'Final Drivers', 'Final Riders', 'Profit for ride', 'Match rate'])

results_df['Margin'] = results_df['Net Revenue'] - results_df['Costs']


fig, ax = plt.subplots() 
ax = plt.plot(test_profits_sm, net_revenue)
st.write(fig)

st.write(results_df)


st.subheader('Simulation of growth function for Toledo Market')
fig, ax = plt.subplots() 
ax = plt.plot(x, drivers)
st.write(fig)





    







