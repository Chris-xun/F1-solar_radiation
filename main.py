import functions as f
import matplotlib.pyplot as plt
import optical_depth_automated as optical

file = r'data\LOG240212-1119.csv'


data = f.import_data(file)
date, time, intensity, temp = data[0], data[1], data[2], data[3]

f.plot_data(time, intensity, temp)
optical.plotting(file)


f.rm()

# abc