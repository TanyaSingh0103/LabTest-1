import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

time = np.arange(0, 1440)
aqis = np.random.randint(60, 100, size=(len(time)))

noise = np.random.rand(len(time)) * 10

aqis = aqis + noise


b, a = signal.butter(3, 0.05, btype='low')
smoothed_aqis = signal.filtfilt(b, a, aqis)


hourly_averages = np.array([np.mean(i) for i in aqis.reshape(-1, 60)])


high_aqi_idx = np.where(aqis > 100)

high_aqis = [aqis[i] for i in high_aqi_idx]

duration = 0
intervals = []
start = 0

for i in range(1, len(high_aqi_idx)):
    if(high_aqi_idx[i] == high_aqi_idx[i - 1]):
        duration += 1
        if(duration >= 15):
            duration = 0
            intervals.append([start,i])
    else:
        start = i
        duration = 0

interval_times = []
interval_aqis = []
for i in intervals:
    for j in range(i[0],i[1] + 1):
        interval_times.append(j)
        interval_aqis.append(aqis[j])
        
    
plt.figure(figsize=(15, 5))
plt.plot(time, aqis, label='Original Data', alpha=0.6)
plt.plot(time, smoothed_aqis, label='Smoothed Data')
plt.scatter(time[::60], hourly_averages, label='Hourly Average', color='black')
plt.scatter(high_aqi_idx, high_aqis, label='High AQI', marker='.', color='red') 
plt.scatter(interval_times, interval_aqis)
plt.legend()
plt.show()
