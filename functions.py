# Description: This file holds useful functions that will be imported by the main program
 
import numpy as np
import matplotlib.pyplot as plt

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
                
    # # importing the data and selecting columns
    # with open('data\\temp', 'r') as f:
    #     data = np.genfromtxt(f, delimiter=';', skip_header=1)
    #     print(index_line)
    
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
    

    
    # if intensity data is provided
    if intensity is not None:
        print('plotting intensity')
        plt.plot(time, intensity)
        plt.xlabel('time')
        time_arr_len = len(time)    
        plt.xticks([time[0], time[int(time_arr_len/3)],time[int(time_arr_len*2/3)],  time[-1]])
        plt.savefig('data\\intensity.png')
        plt.close()
        
    # if temperature data is provided
    if temp is not None:
        plt.plot(time,temp, label='temperature')
        plt.legend()
        plt.xlabel('time')
        time_arr_len = len(time)    
        plt.xticks([time[0], time[int(time_arr_len/3)],time[int(time_arr_len*2/3)],  time[-1]])
        plt.savefig('data\\temp.png')
        plt.close()


    
    
    return None