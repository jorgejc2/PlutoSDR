import numpy as np
import matplotlib.pyplot as plt
from sys import argv
from pluto_lib import PlutoSDR
from scipy import signal
from time import sleep
from threading import Thread

# RXLO = int(914e6) # center frequency to tune to
RXLO = int(2410e6)
RXBW = int(3e6) # bandwidth
RXFS = int(3e6) # sample rate

sdr = PlutoSDR()

sdr.rx_rf_port_select_chan0 = "A_BALANCED"
sdr.rx_lo = RXLO
sdr.sample_rate = RXFS
sdr.gain_control_mode_chan0 = "slow_attack"
sdr.rx_buffer_size = int(30e3)

fft_size = 32768
num_rows = 200

raw_samples = np.zeros((num_rows, 30000), dtype=np.complex64)
rx_samples = np.zeros((num_rows,fft_size), dtype=np.complex64)

#generate 5ms intervals for 1 second
t = np.arange(int(sdr.rx_buffer_size*num_rows))/RXFS
f = np.linspace(RXFS/-2, RXFS/2, len(rx_samples[0]))

for k in range(200):
    raw_samples[k,:30000] = sdr.rx()
print(raw_samples)

rx_samples[:,:30000] = raw_samples[:,:30000]
for i in range(num_rows):
    rx_samples[i,:] = 10*np.log10(np.abs(np.fft.fftshift(np.fft.fft(rx_samples[i], fft_size)))**2)

rx_samples = rx_samples.astype('float64')
# rx_samples.dtype = np.float64

#generates the spectogram
plt.imshow(rx_samples, aspect='auto', extent=[-RXFS/2/21e6, RXFS/2/1e6, 0, 200])
plt.xlabel("Frequency [MHz]")
plt.ylabel("Time [5 ms]")
plt.show()

def transmit_loop(samples):
    counter = 0
    switch = False
    while True:
        # if counter == 200:
        #     counter = 0
        # sdr.tx(samples[counter])
        #using switch instead
        if switch:
            sdr.tx(samples[0])
        else:
            sdr.tx(samples[42])
        switch != switch
        # counter += 1

input("Press Enter to continue...")

#configure tx
sdr.tx_rf_bandwidth = RXBW
sdr.tx_lo = RXLO
sdr.tx_hardwaregain_chan0 = -50

Thread(target=transmit_loop, args=(raw_samples, ), daemon=True).start()

rx_samples = rx_samples.astype('complex64')
# rx_samples.dtype = np.complex64

#throw away data
for i in range(100):
    sdr.rx()

for k in range(200):
    raw_samples[k,:30000] = sdr.rx()
print(raw_samples)

rx_samples[:,:30000] = raw_samples[:,:30000]
for i in range(num_rows):
    rx_samples[i,:] = 10*np.log10(np.abs(np.fft.fftshift(np.fft.fft(rx_samples[i], 32768)))**2)

rx_samples = rx_samples.astype('float64')
# rx_samples.dtype = np.float64

#generates the spectogram
plt.imshow(rx_samples, aspect='auto', extent=[-RXFS/2/21e6, RXFS/2/1e6, 0, 200])
plt.xlabel("Frequency [MHz]")
plt.ylabel("Time [5 ms]")
plt.show()