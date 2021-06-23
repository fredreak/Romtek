# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 08:50:27 2021

@author: G024108
"""



import numpy as np
from scipy.optimize import leastsq
import pylab as plt

# N = 1000 # number of data points
# t = np.linspace(0, 4*np.pi, N)
f = 1.15247 # Optional!! Advised not to use
# data = 3.0*np.sin(f*t+0.001) + 0.5 + np.random.randn(N) # create artificial data with noise


def read_from_file_raw():
    time_pos_array= np.empty((0,2))  #time_pos_array is a 2xN matrix, with pairs of t and x to start with, then tranposed
    try:
        with open("A2_volts_cropped3.txt", 'r') as file_obj: #"A2_volts.txt"
            for line in file_obj:
                to_append = np.array(line.split(","), dtype = float)
                if to_append[1]== np.nan:
                    print("Not a number")
                    continue
                time_pos_array = np.append(time_pos_array, np.array([to_append]), axis=0)
            time_pos_array = time_pos_array.transpose() #Transpose making it a list of times and a list of poisitions
            print("DONE READING")
    except Exception as e:
        print("Error when reading file. Message: \n", e)
    return time_pos_array

time_pos_array = read_from_file_raw()

t = time_pos_array[0]
data = time_pos_array[1]

guess_mean = np.mean(data)
guess_std = 3*np.std(data)/(2**0.5)/(2**0.5)
guess_phase = 0
guess_freq = 1
guess_amp = 1

# we'll use this to plot our first estimate. This might already be good enough for you
data_first_guess = guess_std*np.sin(t+guess_phase) + guess_mean

# Define the function to optimize, in this case, we want to minimize the difference
# between the actual data and our "guessed" parameters
optimize_func = lambda x: x[0]*np.sin(x[1]*t+x[2]) + x[3] - data
est_amp, est_freq, est_phase, est_mean = leastsq(optimize_func, [guess_amp, guess_freq, guess_phase, guess_mean])[0]

# recreate the fitted curve using the optimized parameters
data_fit = est_amp*np.sin(est_freq*t+est_phase) + est_mean

# recreate the fitted curve using the optimized parameters

fine_t = np.arange(0,max(t),0.1)
data_fit=est_amp*np.sin(est_freq*fine_t+est_phase)+est_mean

plt.plot(t, data, '.')
plt.plot(t, data_first_guess, label='first guess')
plt.plot(fine_t, data_fit, label='after fitting')
plt.legend()
plt.show()