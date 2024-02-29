# Xun Yu
# Description: the main program where other modules are imported and used

import functions as f
import matplotlib.pyplot as plt
import optical_depth_automated as optical

file = r'data\LOG240217-0841.csv'


data = f.import_data(file)
date, time, intensity, temp = data[0], data[1], data[2], data[3]

f.plot_data(time, intensity, temp)
optical.plotting(file)



f.rm()



f.cal_A_and_C([0.270, 0.293, 0.393], [0.007, 0.008, 0.01])



# #Calculating Trasnmittivity from SZA & Optical Depths (based on Beer-Lambert Law)
# transmittivities = np.exp(-optical_depth/ np.cos(zenith_angles))
# results = list(zip(zenith_angles, optical_depth, transmittivities))
# # Print the results
# for result in results:
#     print(f"Zenith Angle: {result[0]}, Optical Depth: {result[1]}, Transmittivity: {result[2]:.4f}")