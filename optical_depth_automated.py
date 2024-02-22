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

# def calculate_zenith_angle(initial_time, final_time, initial_angle, change_in_zenith_angle_per_hour):
#     # Convert the times to datetime objects
#     initial_time = datetime.strptime(initial_time, '%H:%M:%S')
#     final_time = datetime.strptime(final_time, '%H:%M:%S')

#     # Calculate the time difference
#     time_difference = final_time - initial_time

#     # Calculate the number of hours between the two times
#     hours = time_difference.total_seconds() / 3600

#     # Create a list of times at 5 second intervals
#     times = [initial_time + timedelta(seconds=5*i) for i in range(int(hours*720))]
#     change_in_zenith_angle_per_interval = 5 * change_in_zenith_angle_per_hour / 3600
#     zenith_angles = []
#     zenith_angles.append(initial_angle)
#     for i in range(1, len(times)):
#         zenith_angles.append(zenith_angles[i-1] + change_in_zenith_angle_per_interval)
        
#     return zenith_angles


# hour_change is the change of zenith angle per hour
def plotting(file):
    # Load the data, assuming the 4th column contains irradiance values and skipping the first 4 rows
    # irr_data = np.loadtxt('C:\Users\aryan\OneDrive - Imperial College London\Physics\Year 3 Lab\Solar Radiation\F1-solar_radiation\data\LOG240215-0945.csv', delimiter=',', skiprows=3, usecols=[3])
    data = f.import_data(file)
    date, time, irr_data, temp = data[0], data[1], data[2], data[3]
    irr_data = np.array([float(i) for i in irr_data])
    initial_time = time[0]
    initial_date = date[0]
    final_time = time[-1]
    final_date = date[-1]
    initial_time = initial_date + ' ' + initial_time
    final_time = final_date + ' ' + final_time
    zenith_angles = f.calculate_solar_zenith_angle(initial_time, final_time)

    # Assume I_0 is known or has been measured/calculated beforehand
    I_0 = 1.367 # mean extra terrestrial irradiance value

    # Calculate air mass for each zenith angle
    air_masses = calculate_air_mass(zenith_angles)

    # Calculate the natural logarithm of the ratio of I/I_0 for each data point
    ln_I_ratio = np.log(irr_data / I_0)

    print(len(air_masses), len(ln_I_ratio), len(time))
    # Plot the data
    plt.plot(air_masses[:len(ln_I_ratio)], ln_I_ratio, 'x')###############################3
    plt.xlabel('Air Mass')
    plt.ylabel('ln(I/I_0)')

    # Perform a linear fit to the data
    coefficients = np.polyfit(air_masses[:len(ln_I_ratio)], ln_I_ratio, 1)###############################3
    slope, intercept = coefficients

    # Calculate the optical depth using the slope of the linear fit
    optical_depth = calculate_optical_depth(slope)

    # Plot the linear fit line
    fit_line = np.polyval(coefficients, air_masses[:len(ln_I_ratio)]) ###############################3
    plt.plot(air_masses[:len(ln_I_ratio)], fit_line, label=f'Linear Fit: Optical Depth = {optical_depth:.2f}', color='red')###############################3
    plt.legend()
    plt.title('Optical Depth vs Air Mass')
    end_points = [fit_line[0], fit_line[len(ln_I_ratio)-1]]   ###############################3
    plt.ylim(min(end_points)-0.05, max(end_points)+0.05)
    plt.savefig('data\\optical_depth.png')

    # Show the plot
    plt.show()


# each 5 second interval is 5/3600=0.00138889 hours
# plotting(r'data\LOG240218-0921.csv')