import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

Fs = 300 # sample rate
Ts = 1/Fs # sample period
N = 1048576 # number of samples to simulate
psd_length = 256

t = Ts*np.arange(N)
x = np.exp(1j*2*np.pi*50*t) # simulate sinusoid at 50 Hz

n = (np.random.randn(N) + 1j*np.random.randn(N))/np.sqrt(2) # complex noise with unity power
noise_power = 2
r = x + n * np.sqrt(noise_power)

PSD = (np.abs(np.fft.fft(r))/N)**2
PSD_log = 10.0*np.log10(PSD)
PSD_shifted = np.fft.fftshift(PSD_log)
f = np.arange(Fs/-2.0, Fs/2.0, Fs/N) # start, stop, step

_, psd = signal.welch(r, Fs, 'hamming', psd_length, return_onesided=True, scaling='density', average='median')
psd_dB = np.fft.fftshift(10*np.log10((np.abs(psd)/psd.shape[0])**2)) + 44  # small miscalculation I made requiring an offset to correct the graph
f_welch = np.linspace(Fs/-2.0, Fs/2.0, psd_length)

plt.figure(figsize=(18,12))
plt.subplot(121)
plt.plot(t, np.sin(2*np.pi*50*t))
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.title("Time Domain")
plt.subplot(122)
plt.plot(f, PSD_shifted, label="FFT")
plt.plot(f_welch, psd_dB, label="Welch")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Magnitude [dB]")
plt.title("Frequency Domain")
plt.grid(True)
plt.legend()
plt.show()