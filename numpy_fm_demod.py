import numpy as np
import scipy.signal as signal

from rtlsdr import RtlSdr


class NumpyFmDemod():
    '''
    Numpy-based FM signal demodulation
    Based on the great tutorial by Fraida Fund
    https://witestlab.poly.edu/blog/capture-and-decode-fm-radio/
    '''
    def __init__(self, frequency, sample_rate=1140000, sample_count=8192000, dc_offset=250000):
        self.freq = int(frequency)
        self.sample_rate = sample_rate
        self.sample_count = sample_count
        self.dc_offset = dc_offset

    def capture_samples(self):
        sdr = RtlSdr()
        sdr.sample_rate = self.sample_rate
        sdr.center_freq = self.freq - self.dc_offset
        sdr.gain = 'auto'
        self.samples = sdr.read_samples(self.sample_count)
        sdr.close()

    def demod(self):
        # Convert samples to a numpy array
        x1 = np.array(self.samples).astype('complex64')

        # Mix the samples back down to avoid DC offset
        fc1 = np.exp(-1.0j * 2.0 * np.pi * self.dc_offset / self.sample_rate * np.arange(len(x1)))
        x2 = x1 * fc1

        # Downsample the signal to catch only the target frequency
        BANDWIDTH = 200000  # wideband FM signal is always 200kHz
        TAPS = 64

        # Use Remez algorithm to design filter coefficients
        lpf = signal.remez(TAPS, [0, BANDWIDTH, BANDWIDTH + (self.sample_rate / 2 - BANDWIDTH) / 4, self.sample_rate / 2], [1,0], Hz=self.sample_rate)
        x3 = signal.lfilter(lpf, 1.0, x2)

        decimation_rate = int(self.sample_rate / BANDWIDTH)
        x4 = x3[0::decimation_rate]
        decimated_rate = self.sample_rate / decimation_rate

        y5 = x4[1:] * np.conj(x4[:-1])
        x5 = np.angle(y5)

        d = decimated_rate * 75e-6  # Calculate the # of samples to hit the -3dB point
        x = np.exp(-1/d)  # Calculate the decay between each sample
        b = [1-x]  # Create the filter coefficients
        a = [1,-x]
        x6 = signal.lfilter(b,a,x5)

        audio_freq = 44100.0
        dec_audio = int(decimated_rate / audio_freq)
        Fs_audio = decimated_rate / dec_audio

        x7 = signal.decimate(x6, dec_audio)

        x7 *= 10000 / np.max(np.abs(x7))
        x7.astype('int16').tofile('wbfm-mono.raw')

    def run(self):
        self.capture_samples()
        self.demod()

if __name__ == '__main__':
    nfd = NumpyFmDemod(frequency=96.3e6)
    nfd.run()
