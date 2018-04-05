import sys
import numpy as np
import scipy.signal as signal

from rtlsdr import RtlSdr


class NumpyFmDemod():
    '''
    Numpy-based FM signal demodulation
    Based on the great tutorial by Fraida Fund
    https://witestlab.poly.edu/blog/capture-and-decode-fm-radio/
    '''
    def __init__(self, frequency, sample_rate=1800000, sample_count=8192000, dc_offset=250000):
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
        self.samples_to_np()
        sdr.close()

    def load_samples(self, filename):
        self.samples = np.load(filename)

    def dump_samples(self, filename):
        np.save(filename, self.samples)

    def decimate(self, rate):
        '''
        Utility function to decimate signal by a given rate
        '''
        self.samples = signal.decimate(self.samples, rate)
        self.sample_rate /= rate

    def samples_to_np(self):
        '''
        Convert samples to a complex numpy array
        '''
        self.samples = np.array(self.samples).astype('complex64')

    def mix_down_dc_offset(self):
        '''
        Mix the samples back down to account for DC offset
        '''
        fc1 = np.exp(-1.0j * 2.0 * np.pi * self.dc_offset / self.sample_rate * np.arange(len(self.samples)))
        self.samples *= fc1

    def lowpass_filter(self):
        '''
        Apply low-pass filter to catch only the target frequency
        '''
        BANDWIDTH = 200000  # wideband FM signal is always 200kHz
        decimation_rate = int(self.sample_rate / BANDWIDTH)
        self.decimate(decimation_rate)

    def polar_discriminator(self):
        '''
        Apply a polar discriminator to demodulate the FM signal
        '''
        self.samples = np.angle(self.samples[1:] * np.conj(self.samples[:-1]))

    def de_emphasis_filter(self):
        '''
        Apply a de-emphasis filter
        Still need to figure out exactly what's going on here
        '''
        d = self.sample_rate * 75e-6
        x = np.exp(-1/d)
        b, a = [1-x], [1,-x]
        self.samples = signal.lfilter(b, a, self.samples)

    def mono_decimate(self):
        '''
        Decimate the signal to catch the mono transmission
        '''
        audio_freq = 44100.0
        decimation_rate = int(self.sample_rate / audio_freq)
        self.decimate(decimation_rate)

    def scale_volume(self):
        '''
        Scale samples to adjust volume
        '''
        self.samples *= 10000 / np.max(np.abs(self.samples))

    def output_file(self, filename, astype='int16'):
        self.samples.astype(astype).tofile(filename)

    def demod(self):
        self.mix_down_dc_offset()
        self.lowpass_filter()
        self.polar_discriminator()
        self.de_emphasis_filter()
        self.mono_decimate()
        self.scale_volume()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: numpy_fm_demod.py <command> [arg]\n')
        exit()
    else:
        cmd = sys.argv[1]
        try:
            arg = sys.argv[2]
        except:
            arg = None

    nfd = NumpyFmDemod(frequency=91.8e6)
    if cmd == 'load':
        nfd.load_samples(arg)
        nfd.demod()
        nfd.output_file(f'wbfm-mono-{nfd.sample_rate}.raw', astype='int16')
    elif cmd == 'capture':
        nfd.capture_samples()
        nfd.demod()
        nfd.output_file(f'wbfm-mono-{nfd.sample_rate}.raw', astype='int16')
    elif cmd == 'dump':
        nfd.capture_samples()
        nfd.dump_samples(arg)
