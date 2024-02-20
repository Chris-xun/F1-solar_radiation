import numpy as np
import matplotlib.pyplot as plt
from math import radians, degrees, sin, cos, acos
from datetime import datetime, timedelta
import functions as f


# Function to calculate air mass given the zenith angle
def calculate_air_mass(zenith_angle):
    return 1 / (np.cos(np.radians(zenith_angle)) + 0.50572*(96.075-zenith_angle)**(-1.6364))

# Function to calculate optical depth given the slope of the linear fit
def calculate_optical_depth(slope):
    return -slope

# Function to update subsolar longitude
def update_subsolar_longitude(initial_longitude, seconds_elapsed):
    # The Earth rotates 360 degrees in 24 hours
    # => 360 degrees in 86400 seconds
    # => 0.00416667 degrees per second
    degrees_per_second = 0.00416667
    new_longitude = (initial_longitude + degrees_per_second * seconds_elapsed) % 360
    return new_longitude

# Assuming we have the subsolar latitude for the day
#subsolar_latitude = 13.47  # Replace every time
#london_lattitude = 51.3
#london_longitude = -0.07
#initial_subsolar_longitude = -0.127758 

hours = 4 #number of hours we recorded the data for

# Update zenith angle every hour
for i in range(0, hours):  # There are 17280 five-second intervals in a day
    start_zenith_angle = radians (63.0047)
    hour_angle = radians (0.1971)
    new_zenith_angle = start_zenith_angle + hour_angle*hours 

# List of all zenith angles
zenith_angles = np.list (new_zenith_angle)  #replace with an array of zenith angles

# Load the data, assuming the 4th column contains irradiance values and skipping the first 4 rows
# irr_data = np.loadtxt('C:\Users\aryan\OneDrive - Imperial College London\Physics\Year 3 Lab\Solar Radiation\F1-solar_radiation\data\LOG240215-0945.csv', delimiter=',', skiprows=3, usecols=[3])
irr_data = f.import_data(r'C:\Users\aryan\OneDrive - Imperial College London\Physics\Year 3 Lab\Solar Radiation\F1-solar_radiation\data\LOG240215-0945.csv')

# Assume I_0 is known or has been measured/calculated beforehand
I_0 = 1367 # mean extra terrestrial irradiance value



# Calculate air mass for each zenith angle
air_masses = calculate_air_mass(zenith_angles)

# Calculate the natural logarithm of the ratio of I/I_0 for each data point
ln_I_ratio = np.log(irr_data / I_0)

# Plot the data
plt.scatter(air_masses, ln_I_ratio)
plt.xlabel('Air Mass')
plt.ylabel('ln(I/I_0)')

# Perform a linear fit to the data
coefficients = np.polyfit(air_masses, ln_I_ratio, 1)
slope, intercept = coefficients

# Calculate the optical depth using the slope of the linear fit
optical_depth = calculate_optical_depth(slope)

# Plot the linear fit line
fit_line = np.polyval(coefficients, air_masses)
plt.plot(air_masses, fit_line, label=f'Linear Fit: Optical Depth = {optical_depth:.2f}', color='red')
plt.legend()

# Show the plot
plt.show()
