# Price model for a ride sharing platform

## Streamlit app
https://lorenzobonomi-platformpricesmodel-main-xq7rwh.streamlitapp.com/

## Assumptions
The model assumes that the market will be saturated at 20% of Toledo population for riders and for drives the saturation is based on a ratio of riders / drivers based on competitors benchmarks (https://therideshareguy.com/uber-statistics/)

The growth of the market is modeled with a logistic function which is typically a good growth approximation. In the streamlit dashboard is possible to change the time required for reaching the market saturation in the number of months.

The model also assumes an initial number of drivers for the market at 100.


## Model calculations for net revenue maximization
In order to develop different scenarios for different pricing points, the relation between the net profit for a ride (assumed to be at $6 for a match rate of 60%) is modeled with a function with diminishing returns: a higher incentive for the driver matches with a higher match rate but the relation is not linear.

The simulation when the first parameter of the streamlit dashboard is set to "Yes" models for acquiring raiders and drivers and related costs.
If the number of riders and drivers is already higher than the modeled growth of the market with the logistic function, the model assumes that is not necessary to acquire new users or drivers.

## Possible development
Some parameters could be simulated assuming a distribution and not a fixed value (e.g 20% of market saturation). A distribution of values could help to model a Montecarlo simulation and give a distribution of potential outcomes.

Churn rates could also be modeled with different values by month by different cohort to have a more accurate evaluation of the impact of factors like seasonality (e.g. drivers or riders starting to use the platform during vacation time) and acquisition channels.




