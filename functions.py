# Description: This file holds useful functions that will be imported by the main program
 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pvlib
from math import radians, degrees, sin, cos, acos

def import_data(filename):
    """
    This function imports data from a file and returns a numpy array
    """
    
    # removing all the text before the data
    with open(filename, 'r') as f:
        lines = f.readlines()
        with open('data\\temp', 'w') as temp:
            for line in lines:
                if 'W/m2' in line:
                    index_line = line
                if '.data;' in line:
                    temp.write(line)
    
    # imorting data, this needs the correct logging setting as recored in onenote
    data = np.loadtxt('data\\temp', delimiter=';', dtype='str')
    date = data[:,1]
    time = data[:,2]
    intensity = data[:,3]
    temperature = data[:,4]
    
    return np.array([date, time, intensity, temperature])

def rm():
    """
    This function removes the temp file
    """
    import os
    os.remove('data\\temp')
    print('temp file removed')
    
    
def plot_data(time, intensity=None, temp=None):
    """
    This function plots the data
    """
    intensity = [float(i) for i in intensity]
    

    
    # if intensity data is provided
    if intensity is not None:
        print('plotting intensity')
        plt.plot(time, intensity)
        
        # setting the x and y ticks
        plt.xlabel('Time', fontsize=12)
        time_arr_len = len(time)    
        plt.xticks([time[0], time[int(time_arr_len/3)],time[int(time_arr_len*2/3)],  time[-1]])
        max_I, min_I = float(max(intensity)), float(min(intensity))
        intensity_interval = (float(max_I) - float(min_I))/10
        intensity_ticks = [min_I + i*intensity_interval for i in range(0,11)]
        plt.yticks(intensity_ticks)
        plt.ylabel('Intensity $ W/m^2 $', fontsize=14)
        
        plt.savefig('data\\intensity.png', dpi=300)
        plt.close()
        
    # if temperature data is provided
    if temp is not None:
        plt.plot(time,temp, label='temperature')
        plt.legend()
        plt.xlabel('time')
        time_arr_len = len(time)    
        plt.xticks([time[0], time[int(time_arr_len/3)],time[int(time_arr_len*2/3)],  time[-1]])
        plt.savefig('data\\temp.png', dpi=300)
        plt.close()

    
    return None




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


def calculate_solar_zenith_angle(initial_time, final_time):
    """
    This function calculates the solar zenith angle
    """
    
    # Define the geographical location (London)
    latitude, longitude = 51.5074, -0.1278

    # Define the time range

    timezone = 'Europe/London'
    times = pd.date_range(initial_time, final_time, freq='5S', tz=timezone)

    # Calculate solar position
    solpos = pvlib.solarposition.get_solarposition(times, latitude, longitude)
    print(times)

    # Extract the Solar Zenith Angle
    sza = solpos['apparent_zenith']
    
    return sza
