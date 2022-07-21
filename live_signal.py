import numpy as np
import matplotlib.pyplot as plt
from sys import argv
from pluto_lib import PlutoSDR
from scipy import signal
from time import sleep
import matplotlib.animation as animation
from sys import argv

# RXLO = int(914e6) # center frequency to tune to
# RXLO = int(2410e6)
# RXLO = int(462e6) # around the frequency of blue radio
# RXLO = int(150e6) # frequency of tdmr radio (burst mode)
RXLO = int(argv[1]) * int(1e6)
RXBW = int(40e6) # bandwidth
RXFS = int(40e6) # sample rate

sdr = PlutoSDR()

sdr.rx_rf_port_select_chan0 = "A_BALANCED"
sdr.rx_lo = RXLO
sdr.sample_rate = RXFS
sdr.gain_control_mode_chan0 = "slow_attack"
sdr.rx_buffer_size = int(40e3)

fft_size = 40000
num_rows = 500

# raw_samples = np.zeros((num_rows, 30000), dtype=np.complex64)
rx_samples = np.zeros((num_rows,fft_size), dtype=np.complex64)

#clean buffer
for i in range(30):
    sdr.rx()

for k in range(500):
    rx_samples[k,:40000] = sdr.rx()

spectogram = np.zeros((500,1024), dtype=np.float64)
for i in range(num_rows):
    _, psd = signal.welch(rx_samples[i,:40000], RXFS, 'flattop', 1024, return_onesided=False, scaling='density', average='median')
    # psd_dB = 10*np.log10((np.abs(psd)/psd.shape[0])**2)
    # psd_dB = 10*np.log10((np.abs(psd)/1024)**2)
    psd_dB = 20 * np.log10(psd)
    spectogram[i,:] = np.fft.fftshift(psd_dB)

#generates the spectogram
left_bound = (RXLO - RXFS/2)/1e6
right_bound = (RXLO + RXFS/2)/1e6
plt.imshow(spectogram, aspect='auto', extent=[left_bound, right_bound, 0, num_rows])
plt.xlabel("Frequency [MHz]")
plt.ylabel("Time [ms]")
plt.show()

frame_counter = 0
f = np.linspace(RXFS/-2, RXFS/2, len(rx_samples[0]))
f = f/1e6
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def iterate_frame(i):
    global frame_counter
    global f
    if frame_counter < num_rows:
        frame = 10*np.log10(np.abs(np.fft.fftshift(np.fft.fft(rx_samples[frame_counter], fft_size)))**2)
        ax1.clear()
        ax1.set_xlabel("Frequency [MHz]")
        ax1.set_ylabel("dB")
        ax1.set_title("Frame {}".format(frame_counter))
        ax1.plot(f,frame)
        frame_counter += 1
    return

# anim = animation.FuncAnimation(fig, iterate_frame, interval = 3000, frames=500, repeat=True)
# plt.show()

frame_counter = 100
frame = 10*np.log10(np.abs(np.fft.fftshift(np.fft.fft(rx_samples[frame_counter], fft_size)))**2)
peak = np.max(frame)
peak -= 30
place_holder = np.zeros((len(frame),))
place_holder += peak

ax1.clear()
ax1.set_xlabel("Frequency [MHz]")
ax1.set_ylabel("dB")
ax1.set_title("Frame {}".format(frame_counter))
ax1.plot(f,frame)
ax1.plot(f,place_holder)

plt.show()