"""
This is a class that builds on the Pluto class to make initialization and setting some attributes easier
"""

from adi import Pluto
from iio import Device

class PlutoSDR(Pluto):
    default_ip_address = "ip:192.168.2.1"
    _rx_lo_channel_name = "altvoltage0"
    _tx_lo_channel_name = "altvoltage1"

    def __init__(self, ip_address: str = default_ip_address):
        super().__init__(ip_address)
    
    @property
    def ip(self) -> str:
        return self._ip 
    @property
    def rxadc(self) -> Device:
        return self._rxadc
    @property
    def txdac(self) -> Device:
        return self._txdac
    @property
    def rx_rf_port_select_chan0(self) -> str:
        return self._get_iio_attr("voltage0", "rf_port_select", False)
    @rx_rf_port_select_chan0.setter
    def rx_rf_port_select_chan0(self, value: str):
        self._set_iio_attr("voltage0", "rf_port_select", False, value)
    @property
    def tx_rf_port_select_chan0(self) -> str:
        return self._get_iio_attr("voltage0", "rf_port_select", True)
    @tx_rf_port_select_chan0.setter
    def tx_rf_port_select_chan0(self, value: str):
        self._set_iio_attr("voltage0", "rf_port_select", True, value)

    """
    This takes a spectogram over a second at 5 ms intervals, best suited for a bandwidth and sample rate of
    3MHz, and buffer size of 30,000 samples
    """
        

    def welch_spectogram(self, RXLO: int, RXBW: int = int(3e6), RXFS: int = int(3e6), BufferSize: int = int(30e3)) -> None:
        try: 
            import matplotlib.pyplot as plt
        except:
            print("Install matplotlib to generate spectogram")
            return
        try:
            import numpy as np
        except:
            print("Install numpy to generate spectogram")
            return
        
        self.rx_rf_port_select_chan0 = "A_BALANCED"
        self.rx_lo = RXLO
        self.sample_rate = RXFS
        self.gain_control_mode_chan0 = "slow_attack"
        self.rx_buffer_size = int(30e3)

        #collect data
        rx_samples = np.zeros((200,32768), dtype=np.complex64)

        for k in range(200):
            rx_samples[k,:30000] = self.rx()

        #generate 5ms intervals for 1 second
        t = np.arange(int(30e3*200))/RXFS

        fft_size = 32768
        num_rows = 200
        # modify this to use welch instead
        for i in range(num_rows):
            rx_samples[i,:] = 10*np.log10(np.abs(np.fft.fftshift(np.fft.fft(rx_samples[i], 32768)))**2)

        rx_samples = rx_samples.astype('float64')

        plt.imshow(rx_samples, aspect='auto', extent=[-RXFS/2/21e6, RXFS/2/1e6, 0, 200])
        plt.xlabel("Frequency [MHz]")
        plt.ylabel("Time [5 ms]")
        plt.show()
        return