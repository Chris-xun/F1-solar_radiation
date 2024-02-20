import numpy as np
import matplotlib.pyplot as plt
from math import radians, degrees, sin, cos, acos
from datetime import datetime, timedelta
import functions as f


# Function to calculate air mass given the zenith angle
def calculate_air_mass(zenith_angle):
    result = []
    for angle in zenith_angle:
        mass = 1 / (np.cos(radians(angle)) + 0.50572*(96.075-angle)**(-1.6364))
        result.append(mass)
    return result

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
subsolar_latitude = 13.47  # Replace every time
london_latitude = 51.5074
london_longitude = 0.1278
initial_subsolar_longitude = -0.127758
current_time = datetime.now()
seconds_elapsed = 0

# Update subsolar point every 5 seconds
for i in range(0, 17280):  # There are 17280 five-second intervals in a day
    subsolar_longitude = update_subsolar_longitude(initial_subsolar_longitude, seconds_elapsed)
    # Here you would call your zenith angle calculation function
    zenith_angle_deg = calculate_zenith_angle(london_latitude, london_longitude, subsolar_latitude, subsolar_longitude)
    
    # Increment the time by 5 seconds
    seconds_elapsed += 5

# Function to calculate zenith angle
def calculate_zenith_angle(london_latitude, london_longitude, subsolar_latitude, subsolar_longitude):
    london_latitude_rad = radians(london_latitude)
    london_longitude_rad = radians(london_longitude)
    subsolar_latitude_rad = radians(subsolar_latitude)
    subsolar_longitude_rad = radians(subsolar_longitude)

    zenith_angle_rad = acos(sin(subsolar_latitude_rad) * sin(london_latitude_rad) +
                            cos(subsolar_latitude_rad) * cos(london_latitude_rad) *
                            cos(london_longitude_rad - subsolar_longitude_rad))

    return degrees(zenith_angle_rad)


# Update subsolar point every 5 seconds
zenith_angles = []
for i in range(0, 17280):  # There are 17280 five-second intervals in a day
    subsolar_longitude = update_subsolar_longitude(initial_subsolar_longitude, seconds_elapsed)
    # Here you would call your zenith angle calculation function
    zenith_angle_deg = calculate_zenith_angle(london_latitude, london_longitude, subsolar_latitude, subsolar_longitude)
    zenith_angles.append(zenith_angle_deg)
    
    
    # Increment the time by 5 seconds
    seconds_elapsed += 5

# Load the data, assuming the 4th column contains irradiance values and skipping the first 4 rows
# irr_data = np.loadtxt('C:\Users\aryan\OneDrive - Imperial College London\Physics\Year 3 Lab\Solar Radiation\F1-solar_radiation\data\LOG240215-0945.csv', delimiter=',', skiprows=3, usecols=[3])
data = f.import_data(r'data\LOG240212-1119.csv')
date, time, irr_data, temp = data[0], data[1], data[2], data[3]
irr_data = np.array([float(i) for i in irr_data])

# Assume I_0 is known or has been measured/calculated beforehand
I_0 = 1.367 # mean extra terrestrial irradiance value

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
