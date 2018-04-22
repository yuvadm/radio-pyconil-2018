import asyncio
import pyaudio
import numpy as np
import scipy.signal as signal

from rtlsdr import RtlSdr



pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16, channels=1, rate=50000, output=True)

async def streaming():
    sdr = RtlSdr()
    sdr.sample_rate = 1.2e6
    sdr.center_freq = 91.8e6

    prev = None

    stream.write(np.array([0] * 100000).astype('int16'))
    stream.start_stream()

    async for samples in sdr.stream():
        samples = np.array(samples).astype('complex64')
        samples = signal.decimate(samples, int(1.2e6 / 200e3))

        if prev is not None:
            samples = np.insert(samples, 0, prev)
        prev = samples[-1]
        samples = np.angle(samples[1:] * np.conj(samples[:-1]))

        x = np.exp(-1 / (200e3 * 75e-6))
        samples = signal.lfilter([1-x], [1,-x], samples)

        samples = signal.decimate(samples, int(200e3 / 50e3))
        samples *= 10000

        stream.write(samples.astype('int16'))

    await sdr.stop()
    sdr.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(streaming())

