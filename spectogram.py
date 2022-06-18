"""
This program uses the PlutoSDR to capture a second of samples and then compute the fft's over 5ms intervals
in order to generate a spectrogram. 
Some things to take into consideration:
    *Since the pluto returns IQ complex samples, it is sufficient for the sample rate to be equal to the bandwidth
    *A bandwidth/sample rate of 3MHz was chosen since the vqd seems to be limited to at least a 2MHz frequency rate
    *The buffer only returns 30,000 samples which is 5ms of samples, but the rx_samples array is zero-padded to 32768 
    which is a power of two so that the fft computation can be done faster
Future considerations:
    *I will create this into a class for testing purposes such as determining if polling one batch of samples and then
    computing the fft repeatedly is more efficient than using daemon threads
    *I will do the computations using Welch's method rather than a regular fft since it is supposedly faster, yet 
    rounds data which may or may not be beneficial
"""

import numpy as np
import matplotlib.pyplot as plt
from sys import argv
from pluto_lib import PlutoSDR



RXLO = int(914e6) # center frequency to tune to
RXBW = int(3e6) # bandwidth
RXFS = int(3e6) # sample rate

#configure receiver settings
sdr = PlutoSDR()

sdr.rx_rf_port_select_chan0 = "A_BALANCED"
sdr.rx_lo = RXLO
sdr.sample_rate = RXFS
sdr.gain_control_mode_chan0 = "slow_attack"
sdr.rx_buffer_size = int(30e3)

#collect data
rx_samples = np.zeros((200,32768), dtype=np.complex64)

for k in range(200):
    rx_samples[k,:30000] = sdr.rx()

#generate 5ms intervals for 1 second
t = np.arange(int(30e3*200))/RXFS

fft_size = 32768
num_rows = 200
for i in range(num_rows):
    rx_samples[i,:] = 10*np.log10(np.abs(np.fft.fftshift(np.fft.fft(rx_samples[i], 32768)))**2)

rx_samples = rx_samples.astype('float64')

plt.imshow(rx_samples, aspect='auto', extent=[-RXFS/2/21e6, RXFS/2/1e6, 0, 200])
plt.xlabel("Frequency [MHz]")
plt.ylabel("Time [5 ms]")
plt.show()
