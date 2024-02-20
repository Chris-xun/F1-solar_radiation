import functions as f
import matplotlib.pyplot as plt


data = f.import_data(r'data\LOG240212-1119.csv')
date, time, intensity, temp = data[0], data[1], data[2], data[3]

f.plot_data(time, intensity, temp)

f.rm()

# abc