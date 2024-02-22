import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt


# diffusive flux data 
time_02_16 = np.array(['09:54:00', '09:59:00', '10:04:00', '10:19:00', '10:44:00', '10:49:00'])
total_02_16 = np.array([9.62, 9.18, 6.2, 10.88, 9.92, 10.28])
diffusive_02_16 = np.array([6.35, 4.84, 5.89, 7.56, 6.3, 8.89])

time_02_17 = np.array(['08:43:00', '09:09:00', '09:55:00', '14:14:00', '16:11:00'])
total_02_17 = np.array([2.383, 3.61, 6.73,8.26,1.864])
diffusive_02_17 = np.array([0.663,2.042,3.62,4.72,0.917,])

time_18_02_2024 = np.array(['09:15:00', '09:54:00', '11:13:00', '13:12:00', '15:48:00', '17:11:00', '17:54:00'])
total_Klux_18_02_2024 = np.array([1.925, 9.12, 12.82, 10.16, 3.613, 0.593, 0.0008])
diffusive_18_02_2024 = np.array([1.319, 3.62, 8.02, 6.22, 1.496, 0.278, 0.0002])

times = [time_02_16, time_02_17, time_18_02_2024]
total = [total_02_16, total_02_17, total_Klux_18_02_2024]
diffusive = [diffusive_02_16, diffusive_02_17, diffusive_18_02_2024]


def scaling(times, total, diffusive, plotting=False):
    direct = []
    ratio = []
    for i in range(len(times)):
        direct.append(total[i] - diffusive[i])
        ratio.append(direct[i] / total[i])
        if plotting:
            plt.plot(times[i], direct[i], label='direct flux')
            plt.plot(times[i], diffusive[i], label='diffusive flux')
            plt.plot(times[i], total[i], label='total flux')
            plt.plot(times[i], ratio[i], label='ratio')
            plt.legend()
            plt.show()
    # if plotting:
    #     plt.show()
    return direct, ratio

def time_to_seconds(timestring):
    """Convert time string to seconds from the start of the day."""
    timestring = [str(t) for t in timestring]
    return np.array([((datetime.strptime(time, '%H:%M:%S') - datetime.strptime('00:00:00', '%H:%M:%S')).total_seconds()) for time in timestring])


def cal_direct_from_data(times, total, diffusive):
    """Interpolate the direct flux ratio at 5-second increments."""
    direct_flux = []
    for t, tot, diff in zip(times, total, diffusive):
        # Convert time to seconds
        time_in_seconds = time_to_seconds(t)
        # Calculate direct and ratio
        direct, ratio = scaling(t, tot, diff)
        # Create interpolation function
        interp_func = interp1d(time_in_seconds, ratio, kind='linear', fill_value='extrapolate')
        # Interpolate at 5-second intervals
        time_5_sec_intervals = np.arange(time_in_seconds[0], time_in_seconds[-1], 5)
        interpolated_ratios = interp_func(time_5_sec_intervals)
        direct_flux_ratio.append(interpolated_ratios)
    
    # Flatten the list if you want a single array with all interpolated values
    direct_flux_ratio = np.concatenate(direct_flux_ratio)
    return direct_flux_ratio



# Call the function to calculate direct flux ratios
interpolated_direct_flux = cal_direct_from_data(times, total, diffusive)

# We can print or plot the interpolated direct flux
print(interpolated_direct_flux)
plt.plot(interpolated_direct_flux)
plt.show()