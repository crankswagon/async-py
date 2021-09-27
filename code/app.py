import json
import aiohttp
import asyncio
import time
import traceback

async def hit_api(session, tar):
    async with session.get(tar['url']) as response:        
        await response.text()
        await asyncio.sleep(tar['lagsim']) #simulate some data processing lag here
        return f"{tar['url']} responded at {response.headers.get('Date')}.... data processing finished at {time.strftime('%X')}"

async def main(_targets):
    """
    adapted from this example: https://github.com/geeogi/async-python-lambda-template/tree/master
    aiohttp: https://docs.aiohttp.org/en/stable/
    asyncio: https://docs.python.org/3/library/asyncio.html
        
    """
    print(f"started at {time.strftime('%X')}")
    
    async with aiohttp.ClientSession() as session:
        responses = await asyncio.gather(*[hit_api(session, x) for x in _targets]
                                         ,return_exceptions=True
                                         )

    print(responses)

    print(f"finished at {time.strftime('%X')}")

def lambda_handler(event, context):
    targets=event["target_group"]
    asyncio.run(main(targets))
    