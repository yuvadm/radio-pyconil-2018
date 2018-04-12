import asyncio
import numpy as np
import scipy.signal as signal

from rtlsdr import RtlSdr


async def streaming():
    sdr = RtlSdr()
    sdr.sample_rate = 1800000
    sdr.center_freq = 91.8e6

    audio = None
    i = 0

    async for samples in sdr.stream():
        samples = np.array(samples).astype('complex64')
        samples = signal.decimate(samples, int(1800000 / 200000))
        samples = np.angle(samples[1:] * np.conj(samples[:-1]))
        samples = signal.decimate(samples, int(200000 / 44100))
        samples *= 10000

        if audio is not None:
            audio = np.append(audio, samples.astype('int16'))
        else:
            audio = samples.astype('int16')

        i += 1
        if i > 200:
            break
        else:
            print(len(audio))

    audio.tofile('test.out')
    await sdr.stop()
    sdr.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(streaming())

