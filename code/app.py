import json
import aiohttp
import asyncio
import time
import traceback


async def hit_api(session, url, **kwargs):
    async with session.get(url) as response:        
        await response.text()
        await asyncio.sleep(kwargs["_lagsim"]) #simulate some data processing lag here
        return f"{url} responded at {response.headers.get('Date')}.... data processing finished at {time.strftime('%X')}"



async def main():
    """
    adapted from this example: https://github.com/geeogi/async-python-lambda-template/tree/master
    aiohttp: https://docs.aiohttp.org/en/stable/
    asyncio: https://docs.python.org/3/library/asyncio.html
        
    """
    print(f"started at {time.strftime('%X')}")

    async with aiohttp.ClientSession() as session:
        coroutines = [
            hit_api(session, 'https://google.com', _lagsim = 5),
            hit_api(session, 'https://facebook.com', _lagsim = 10)
        ]
        results = await asyncio.gather(*coroutines, return_exceptions=True)
    
    err = None
    for result, coro in zip(results, coroutines):
        if isinstance(result, Exception):
            err = result
            print(f"{coro.__name__} failed:")
            traceback.print_exception(type(err), err, err.__traceback__)

    if err:
        raise RuntimeError("derp something went wrong")
    
    print(results)

    print(f"finished at {time.strftime('%X')}")

def lambda_handler(event, context):
    asyncio.run(main())
    