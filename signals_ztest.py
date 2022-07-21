import numpy as np
import os.path
import matplotlib.pyplot as plt
from math import sqrt

rxlo = 0
rxfs = 0
rxbw = 0
buf_size = 0
psd_len = 0

f = np.linspace(-(rxfs/2), (rxfs/2), psd_len)
f = (f + rxlo) / 1e6

threshold = 0

for i in range(len(dir_list)):
    file = dir_list[i]
    sets[i] = np.fromfile(path + file, np.float32)
    mean[i] = f[np.argmax(sets[i])]
    indices = np.where(sets[i] > threshold)[0]
    num_datapts[i] = len(indices)
    sum = 0
    if len(indices) > 0:
        for j in range(len(indices)):
            idx = indicies[j]
            sum += abs(mean[i] - f[idx])**2
        std_dev[i] = sqrt(sum/len(indices))
        if i > 0:
            x1 = mean[0]
            x2 = mean[i]
            omega1 = std_dev[0]/sqrt(num_datapts[0])
            omega2 = std_dev[i]/sqrt(num_datapts[i])
            z_vals[i-1] = (abs(x1-x2)/sqrt(omega1 ** 2 + omega2 ** 2))