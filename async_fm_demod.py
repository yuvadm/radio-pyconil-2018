import asyncio
import alsaaudio
import numpy as np
import scipy.signal as signal

from rtlsdr import RtlSdr


device = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, device='default')
device.setchannels(1)
device.setrate(50000)
device.setformat(alsaaudio.PCM_FORMAT_S16_LE)
device.setperiodsize(5520)


async def streaming():
    sdr = RtlSdr()
    sdr.sample_rate = 1.2e6
    sdr.center_freq = 91.8e6

    async for samples in sdr.stream():
        samples = np.array(samples).astype('complex64')
        samples = signal.decimate(samples, int(1.2e6 / 200e3))
        samples = np.angle(samples[1:] * np.conj(samples[:-1]))

        x = np.exp(-1 / (200e3 * 75e-6))
        samples = signal.lfilter([1-x], [1,-x], samples)

        samples = signal.decimate(samples, int(200e3 / 50e3))
        samples *= 10000

        device.write(samples.astype('int16'))

    await sdr.stop()
    sdr.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(streaming())

