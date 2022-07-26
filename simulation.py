import numpy as np
from scipy.special import expit

# Function for simulating profit for ride and match rate
def simulation_match_rate(min_profit, max_profit, n_data_points):

    x = np.linspace(min_profit, max_profit, n_data_points)
    y = 0.09 * np.log(0.5 * x) + 0.87
    
    return (6 - x).tolist(), y.tolist()


# Function to simulate logistic growth for the market
def simulation_acquisition_users(initial, final, n_months_to_saturate_market):

    x = np.linspace(0, 1, n_months_to_saturate_market)
    y = 1 / (1 + np.exp(-(10 * (x - 0.5))))
    y_norm = 1 * (y - min(y))/(max(y) - min(y))

    n_users_market = np.linspace(initial, final, n_months_to_saturate_market)
    n_users_market_growth = n_users_market * y_norm

    return (x * 100).tolist(), y_norm.tolist(), n_users_market_growth.tolist()
