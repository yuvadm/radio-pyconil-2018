import numpy as np
import scipy.signal as signal

from rtlsdr import RtlSdr


class NumpyFmDemod():
    '''
    Numpy-based FM signal demodulation
    Based on the great tutorial by Fraida Fund
    https://witestlab.poly.edu/blog/capture-and-decode-fm-radio/
    '''
    def __init__(frequency, sample_rate=1140000, sample_count=8192000, dc_offset=250000):
        self.freq = int(frequency)
        self.sample_rate = sample_rate
        self.sample_count = sample_count
        self.dc_offset = dc_offset

    def capture_samples(self):
        sdr = RtlSdr()
        sdr.sample_rate = self.sample_rate
        sdr.center_freq = self.freq - self.dc_offset
        sdr.gain = 'auto'

        samples = sdr.read_samples(self.sample_count)
        sdr.close()

        self.raw_samples = np.array(samples).astype('complex64')


if __name__ == '__main__':
    nfd = NumpyFmDemod(frequency=96.3e6)
    nfd.run()
