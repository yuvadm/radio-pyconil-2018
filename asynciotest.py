import asyncio

async def echo():
    pass

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_forever(echo())
