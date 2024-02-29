# Xun Yu
# Description: This file holds functions that are used to perform optical depth related calculations and graphings from the data

import numpy as np
import matplotlib.pyplot as plt
from math import radians, degrees, sin, cos, acos
from datetime import datetime, timedelta
import functions as f
import cal_direct_flux as cdf


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


def calculations_for_plotting():
    # takes the data & performs the plotting by hour or can just chnage the input files
    pass

def plot_clear_sky(x):
    m, c =  -0.17716701548618222, -3.291693589488445
    x = np.array(x)
    y = m * x + c
    
    plt.plot(x, y, label='Optical Depth for Clear Sky : $0.177 \pm 0.004$ ' , color = 'red')


def plotting(file):
    # Load the data, assuming the 4th column contains irradiance values and skipping the first 4 rows
    # irr_data = np.loadtxt('C:\Users\aryan\OneDrive - Imperial College London\Physics\Year 3 Lab\Solar Radiation\F1-solar_radiation\data\LOG240215-0945.csv', delimiter=',', skiprows=3, usecols=[3])
    data = f.import_data(file)
    date, time, irr_data, temp = data[0], data[1], data[2], data[3]
    irr_data = np.array([float(i) for i in irr_data])
    
    
    #test that the data is continous and at 5 second intervals
    xxx = cdf.time_to_seconds(time)
    for i in range(len(xxx)-2):
        if xxx[i+1] - xxx[i] != 5:
            print('data not continous at',time[i])
    
    
    irr_data_direct = cdf.cal_direct_from_data(time, irr_data, file)
    initial_time = time[0]
    initial_date = date[0]
    final_time = time[-1]
    final_date = date[-1]
    initial_time = initial_date + ' ' + initial_time
    final_time = final_date + ' ' + final_time
    zenith_angles = f.calculate_solar_zenith_angle(initial_time, final_time)
    
    
    


    # Assume I_0 is known or has been measured/calculated beforehand
    I_0 = 1361 # mean extra terrestrial irradiance value - acurate to 0.1% 

    # Calculate air mass for each zenith angle
    air_masses = calculate_air_mass(zenith_angles)


    # errors
    error_factor = 10
    error_factor_2 = 1
    # the most zenith angle can change in 5s is ~ 0.013 degrees in london => allow for 0.013/2 degrees error on zenith angles
    angles_err_small = calculate_air_mass(zenith_angles-0.013/2)
    angles_err_big = calculate_air_mass(zenith_angles+0.013/2)
    air_masses_err = (np.array(angles_err_big) - np.array(angles_err_small))/2
    


    # Calculate the natural logarithm of the ratio of I/I_0 for each data point
    ln_I_ratio = np.log(irr_data / I_0)
    ln_I_ratio_max = np.log(irr_data+0.05 / (I_0 - 1))
    ln_I_ratio_min = np.log(irr_data-0.05 / (I_0 + 1))
    ln_I_ratio_err = (ln_I_ratio_max - ln_I_ratio_min)/2
    air_masses = np.array(air_masses)

    # Plot the data
    plt.errorbar(air_masses, ln_I_ratio, fmt='x', label='Intensity Data', yerr=ln_I_ratio_err*error_factor*error_factor_2, xerr=air_masses_err*error_factor, ecolor='black')
    plt.xlabel('Air Mass Ratio = $X \\approx sec (\phi)$', fontsize=12)
    plt.ylabel('$ln( I / I_0 )$', fontsize=14)

    # Perform a linear fit to the data
    coefficients, cov = np.polyfit(air_masses, ln_I_ratio, 1, cov=True)
    slope, intercept = coefficients
    print('cov', cov, 'error on slope', np.sqrt(cov[0,0])  , 'proportional error ', np.sqrt(cov[0,0])/slope)

    # Calculate the optical depth using the slope of the linear fit
    optical_depth = calculate_optical_depth(slope)

    # Plot the linear fit line
    fit_line = np.polyval(coefficients, air_masses)
    plt.errorbar(air_masses, fit_line, label=f'Linear Fit: Optical Depth = {optical_depth:.2f}', color='red')
    plt.legend()
    # plt.title('Optical Depth vs Air Mass')
    end_points = [fit_line[0], fit_line[-1]]
    # plt.ylim(min(end_points)-0.05, max(end_points)+0.05)
    plt.savefig('data\\optical_depth.png', dpi=300)
    plt.close()
    # Show the plot
    # plt.show()
    
    
    
    # for direct irr only
    if 0.0 in irr_data_direct:
        print('0.0 in irr_data_direct')

    ln_I_ratio = np.log(irr_data_direct / I_0)
    ln_I_ratio_max = np.log(irr_data_direct+0.05 / (I_0 - 1))
    ln_I_ratio_min = np.log(irr_data_direct-0.05 / (I_0 + 1))
    ln_I_ratio_err = (ln_I_ratio_max - ln_I_ratio_min)/2
    # Plot the data
    plt.errorbar(air_masses, ln_I_ratio, fmt='x', label='Intensity Data', yerr=ln_I_ratio_err*error_factor*error_factor_2, xerr=air_masses_err*error_factor, ecolor='black')
    plt.xlabel('Air Mass Ratio $= X $', fontsize=12)
    plt.ylabel('ln $( I \hspace{0.2} / \hspace{0.2} I_0 )$', fontsize=14)

    # Perform a linear fit to the data
    coefficients = np.polyfit(air_masses, ln_I_ratio, 1)
    slope, intercept = coefficients
    print('slope', slope, 'intercept', intercept)

    # Calculate the optical depth using the slope of the linear fit
    optical_depth = calculate_optical_depth(slope)

    # Plot the linear fit line
    fit_line = np.polyval(coefficients, air_masses)
    # plt.errorbar(air_masses, fit_line, label=f'Linear Fit: Optical Depth = {optical_depth:.2f}', color='red')
    plot_clear_sky(air_masses)  
    plt.legend()
    # plt.title('Optical Depth vs Air Mass')
    end_points = [fit_line[0], fit_line[-1]] 
    # plt.ylim(min(end_points)-0.05, max(end_points)+0.05)
    plt.savefig('data\\optical_depth_direct.png', dpi=300)
    plt.close()


# each 5 second interval is 5/3600=0.00138889 hours
# plotting(r'data\LOG240218-0921.csv')