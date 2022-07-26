import math

# Function for simulating revenue and margin when selected based on parameters selected
def calculate_net_revenue(option_acquisition, drivers, riders, cac_driver, cac_rider, start_drivers, initial_riders_ratio, test_profits_sm, test_match_rates_sm, rides_month_rider, rides_month_driver, churn_rate_driver, churn_rate_rider_success, churn_rate_rider_failed):
    

    revenue = []
    costs = []
    final_drivers = []
    final_riders = []
    acquired_drivers_list = []
    acquired_riders_list = []
    
    # Loop for the 12 months selected
    for z in range(0, len(test_profits_sm)):

        start_riders = start_drivers * initial_riders_ratio 
        new_drivers = start_drivers 
        new_riders = start_riders
        test_match_rate = test_match_rates_sm[z]

        total_cost_acquisition = 0
        
        net_revenue_start_month = test_profits_sm[z] * start_riders * rides_month_rider * test_match_rates_sm[z]
        net_revenue = net_revenue_start_month

        for i in range(1, 12):
            
            new_drivers -= math.floor(new_drivers * churn_rate_driver)

            if option_acquisition == 'Yes' and (drivers[i] - new_drivers) > 0:
                acquired_drivers = drivers[i] - new_drivers
            else:
                acquired_drivers = 0

            acquired_drivers_list.append(acquired_drivers)
            new_drivers += acquired_drivers
            total_cost_acquisition += acquired_drivers * cac_driver


            new_riders -= math.floor(new_riders * test_match_rate * churn_rate_rider_success + new_riders * (1 - test_match_rate) * churn_rate_rider_failed)
            
            if option_acquisition == 'Yes' and (riders[i] - new_riders) > 0:    
                acquired_riders = riders[i] - new_riders
            else:
                acquired_riders = 0

            acquired_riders_list.append(acquired_riders)
            new_riders += acquired_riders
            total_cost_acquisition += acquired_riders * cac_rider

            new_available_rides = new_drivers * rides_month_driver
            check_rides = new_available_rides - new_riders * rides_month_rider
            if check_rides < 0:
                exit

            net_revenue_new_month = test_profits_sm[z] * new_riders * rides_month_rider * test_match_rates_sm[z]
            net_revenue += net_revenue_new_month
    
        revenue.append(net_revenue)
        costs.append(total_cost_acquisition)
        final_drivers.append(new_drivers)
        final_riders.append(new_riders)
    
    return revenue, costs, final_drivers, final_riders, acquired_drivers_list, acquired_riders_list
    

    


