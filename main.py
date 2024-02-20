import functions as f
import matplotlib.pyplot as plt


date, time, intensity, temp = f.import_data(r'data\LOG240217-0841.csv')

f.plot_data(time, intensity, temp)

f.rm()

# abc