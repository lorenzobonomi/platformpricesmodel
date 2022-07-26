### Modules for project

# Standard modules
from json import load
import numpy as np
import pandas as pd
import streamlit as st
from matplotlib import pyplot as plt
import seaborn as sns
import altair as alt

# Ad-hoc project modules
import price as pr
import simulation as sm
from parameters import initial_riders_ratio, toledo_population,  saturation_riders, saturation_drivers


### App

## Streamlit layout main parameters
st.set_page_config(layout = 'wide')
st.title('Price simulator for ride sharing platform in Toledo, Ohio.')
st.subheader('')

## Streamlit sidebar for data entry and parameters for simulation
with st.sidebar:

    # Form for data entry
    with st.form('myform'):

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
     
        st.form_submit_button('Relaunch Simulation')
     

## Streamlit simulation dashboard

# Columns for max results of simulations
col1, col2, col3, col4  = st.columns(4)

# Simulation of logistic function for market saturation
x, y, drivers = sm.simulation_acquisition_users(start_drivers, saturation_drivers, n_months_to_saturate_market)
x, y, riders = sm.simulation_acquisition_users(start_drivers * initial_riders_ratio, saturation_riders, n_months_to_saturate_market)


# Section for organizing charts for simulations
col5, col6, col7 = st.columns(3)

# Simulation for profit rates and match rates
test_profits_sm, test_match_rates_sm = sm.simulation_match_rate(0.1, 5.9, n_simulations)

# Chart wit simulated profit rates and matrch rates
fig, ax = plt.subplots() 
ax.plot(test_profits_sm, test_match_rates_sm, color = 'red')
ax.set_title('Simulated prices and match rates')
ax.set_ylabel('Match rate')
ax.set_xlabel('Prices')
col5.pyplot(fig)

# Calculation of net revenue and costs when option is selected
net_revenue, costs, final_drivers, final_riders, acquired_drivers, acquired_riders = pr.calculate_net_revenue(option_acquisition, drivers[0:n_months+1], riders[0:n_months+1], cac_driver, cac_rider, start_drivers, initial_riders_ratio, test_profits_sm, test_match_rates_sm, rides_month_rider, rides_month_driver, churn_rate_driver, churn_rate_rider_success, churn_rate_rider_failed)

# Dataframe with results of simulation
results_df = pd.DataFrame(list(zip(net_revenue, costs, final_drivers, final_riders, test_profits_sm, test_match_rates_sm, acquired_drivers, acquired_riders)),
            columns =['Net Revenue', 'Costs', 'Final Drivers', 'Final Riders', 'Profit for ride', 'Match rate', 'Acquired Drivers', 'Acquired Riders'])

results_df['Margin'] = results_df['Net Revenue'] - results_df['Costs']

# Plot of net revenue with profits
fig, ax = plt.subplots() 
ax.plot(test_profits_sm, net_revenue, color = 'blue')
ax.set_title('Simulated net revenue')
ax.set_ylabel('Total Revenue')
ax.set_xlabel('Prices')
col6.pyplot(fig)

# Plot of simulated market saturation
fig, ax = plt.subplots()

ax.plot(x, drivers, color = 'green')
ax.set_title('Simulated growth of the market')
ax.set_ylabel('Riders')
ax.set_xlabel('Months')
col7.pyplot(fig)

# Section for calculating max values of revenue and prices
max_revenue = results_df['Net Revenue'].max()
max_revenue_index = results_df['Net Revenue'].idxmax()
max_revenue_profit = results_df['Profit for ride'].iloc[max_revenue_index]

if option_acquisition == 'No':
    max_margin = 0
    max_margin_profit = 0
else:
    max_margin = results_df['Margin'].max()
    max_margin_index = results_df['Margin'].idxmax()
    max_margin_profit = results_df['Profit for ride'].iloc[max_margin_index]

# Display max values at the top of the dashboard
col1.metric("Max Net Revenue", ('$  {:,}'.format(int(max_revenue))))
col2.metric("Profit for Max Net Revenue", ('$ {}'.format(round(max_revenue_profit, 2))))
col3.metric("Max Margin", ('$  {:,}'.format(int(max_margin))))
col4.metric("Profit for Max Margin", ('$ {}'.format(round(max_margin_profit, 2))) )

# Show full dataframe
st.table(results_df)




    







