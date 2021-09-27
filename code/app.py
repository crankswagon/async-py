import httpx
import asyncio
import time

async def hit_api(client, tar):
    resp = await client.get(tar['url'])
    await asyncio.sleep(tar['lagsim']) #simulate some data processing lag here
    return f"{tar['url']} responded at {resp.headers.get('Date')}.... data processing finished at {time.strftime('%X')}"


async def main(_targets):
    """
    adapted from this example: https://github.com/geeogi/async-python-lambda-template/tree/master
    aiohttp: https://docs.aiohttp.org/en/stable/
    asyncio: https://docs.python.org/3/library/asyncio.html
        
    """
    print(f"started at {time.strftime('%X')}")
    
    async with httpx.AsyncClient() as client:
        responses = await asyncio.gather(*[hit_api(client, x) for x in _targets]
                                         ,return_exceptions=True
                                         )

    print(responses)

    print(f"finished at {time.strftime('%X')}")

def lambda_handler(event, context):
    targets=event["target_group"]
    asyncio.run(main(targets))
    