import asyncio
from rtlsdr import RtlSdr

RATE_IN = RATE_OUT = 170000
RATE_OUT2 = 32000
CUSTOM_ATAN = 1
DEEMPH = 1
SQUELCH = 0

async def streaming():
    sdr = RtlSdr()

    async for samples in sdr.stream():
        # do something with samples
        # ...
        print(len(samples), samples[0])

    # to stop streaming:
    await sdr.stop()

    # done
    sdr.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(streaming())

