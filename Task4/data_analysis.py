import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv(
                        "/Users/stefan/Desktop/F519607_25WSA032_Coursework_V1103/Task4/arduino_output.csv",
                        skipinitialspace=True
                   )
data.columns= ["time", "temperature"]

time= data["time"].to_numpy()
temperaturee = data["temperature"].to_numpy()

sample_interval =np.mean(np.diff(time))
sample_rate = 1/sample_interval


#use fft to analise freuency 
values = np.fft.rfft(temperaturee)
frequency = np.fft.rfftfreq(len(temperaturee), d= sample_interval)
magnitude = np.abs(values)


#temp vs time
plt.figure()
plt.plot(time, temperaturee)
plt.xlabel("Time s")
plt.ylabel("Temp °C")
plt.title("Temp v s time")
plt.savefig("temperature_vs_time.png")
plt.show()


#mag vs frequency 
plt.figure()
plt.plot(frequency, magnitude)
plt.xlabel("Frequency Hz")
plt.ylabel("Magnitude")
plt.title("MAgintude vs Frequwency")
plt.savefig("freq_vs_mag.png")
plt.show()

#smooth temp vs time 
window_value= 5
smoothed_temp = pd.Series(temperaturee).rolling(window=window_value).mean()
plt.figure()
plt.plot(time, temperaturee, label="Original")
plt.plot(time, smoothed_temp, label="Smoothed Temp")
plt.xlabel("Time s")
plt.ylabel("Temp °C")
plt.title("Temp v s time")
plt.savefig("smooth_temperature_vs_time.png")
plt.show()

#histogram 
plt.figure()
plt.hist(temperaturee)
plt.xlabel("Temperature °C")
plt.ylabel("Frequency")
plt.title("Histogram of temperature readings")
plt.savefig("histogram.png")
plt.show()


#rate of change of temperature 
rate_of_change = np.diff(temperaturee)/np.diff(time)
rate_of_change_of_time = time[1:]

plt.figure()
plt.plot(rate_of_change_of_time, rate_of_change)
plt.xlabel("Time s")
plt.ylabel("Temperaature rate of chnage  °C")
plt.title("Temp rate of change  v s time")
plt.savefig("rate_temperature_vs_rate_time.png")
plt.show()