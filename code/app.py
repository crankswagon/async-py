import aiohttp
import asyncio
import time



async def hit_api(session, tar):
    async with session.get(tar['url']) as response:        
        await response.text()
        await asyncio.sleep(tar['lagsim']) #simulate some data processing lag here
        print (f"{tar['metadata']}  |||| {tar['url']} responded at {response.headers.get('Date')}.... data processing finished at {time.strftime('%X')}")



async def hit_api_group(sites):
    """
    this spawns a common session which is used to call the hit_api function
    
    """
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(*[hit_api(session, x) for x in sites]
                                         ,return_exceptions=True
                                         )

        

async def main(_targets):
    """
    adapted from this example: https://github.com/geeogi/async-python-lambda-template/tree/master
    aiohttp: https://docs.aiohttp.org/en/stable/
    asyncio: https://docs.python.org/3/library/asyncio.html

    for each target_group, make its own task with accompaying sessions, so that the # of sessions is dictated by number of target groups in lambda event
        
    """
    print(f"started at {time.strftime('%X')}")
    
    results= [asyncio.create_task(hit_api_group(target)) for target in _targets]
    await asyncio.gather(*results)

    print(results)

    print(f"finished at {time.strftime('%X')}")

def lambda_handler(event, context):
    targets=event["target_groups"]
    asyncio.run(main(targets))
    