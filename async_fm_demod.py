import asyncio
from rtlsdr import RtlSdr

async def streaming():
    sdr = RtlSdr()

    async for samples in sdr.stream():
        print(len(samples), samples[0], type(samples[0]))

    await sdr.stop()

    sdr.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(streaming())

