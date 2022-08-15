import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def signal_generator(freq: list, seconds: int, sample_rate: int, noise_power: int = 2):
    """
    Description: Generates complex iq samples given a list of frequencies
    Inputs: freq: list -- list of frequencies
            seconds: int -- how long the signal activity should be
            noise_power: int -- how prominent the noise should be
    Outputs: None
    Returns: t -- time axis in seconds
             r -- complex iq samples
    """
    Ts = 1/sample_rate # sample period
    ns = int(seconds/Ts) # number of samples to generate
    t = Ts*np.arange(ns)

    n = (np.random.randn(ns) + 1j*np.random.randn(ns))/np.sqrt(2) # complex noise with unity power
    noise_power = 2
    r = n * np.sqrt(noise_power)
    for f in freq:
        r += np.exp(1j*2*np.pi*f*t)
    return t, r

if __name__ == "__main__":

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

    _, psd = signal.welch(r, Fs, 'hamming', psd_length, return_onesided=False, scaling='density', average='median')
    psd_dB = np.fft.fftshift(10*np.log10((np.abs(psd)/psd.shape[0])**2)) + 44  # small miscalculation I made requiring an offset to correct the graph
    f_welch = np.linspace(Fs/-2.0, Fs/2.0, psd_length)

    x1_freq = [-5000000]
    x1_sample_rate = 40000000
    x1_seconds = 1
    x1_psd_length = 1024
    x1, y1 = signal_generator(x1_freq, x1_seconds, x1_sample_rate)
    _, x1_psd = signal.welch(y1, x1_sample_rate, 'hamming', x1_psd_length, return_onesided=False, scaling='density', average='median')
    x1_psd_dB = np.fft.fftshift(10*np.log10((np.abs(x1_psd)/x1_psd.shape[0])**2)) + 150
    x1_f_welch = (np.linspace(x1_sample_rate/-2.0, x1_sample_rate/2.0, x1_psd_length)/1e6)
    # x1_fft = np.fft.fftshift(10.0*np.log10(np.abs(np.fft.fft(y1)/len(y1))**2))
    # x1_f = np.arange(x1_sample_rate/-2.0, x1_sample_rate/2.0, Fs/len(y1))

    plt.figure(figsize=(12,10))
    plt.subplot(221)
    plt.plot(t, r)
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.title("Time Domain")
    plt.subplot(222)
    plt.plot(f, PSD_shifted, label="FFT")
    # plt.plot(f_welch, psd_dB, label="Welch")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Magnitude [dB]")
    plt.title("Frequency Domain")
    plt.grid(True)
    plt.legend()
    plt.subplot(223)
    plt.plot(x1,y1)
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.title("Time Domain")
    plt.subplot(224)
    plt.plot(x1_f_welch,x1_psd_dB)
    plt.xlabel("Frequency [MHz]")
    plt.ylabel("Magnitude [dB]")
    plt.title("Frequency Domain")
    plt.grid(True)
    plt.show()