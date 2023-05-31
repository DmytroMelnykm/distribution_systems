from aiohttp import ClientSession
from asyncio import new_event_loop, sleep


async def get_massage_from_service(domain: str, url: str = "/", method: str = "GET", json: dict = None) -> dict:
    async with ClientSession(domain) as session:
        async with session.request(url=url, method=method, json=json) as response:
            response.raise_for_status()
            return await response.json()
        

async def send_message(adress):
    for number in range(15):
        await get_massage_from_service(
                domain=adress,
                method="POST",
                json={
                    "message": f"messgae num {number}"
                }
            )


async def get_all_massage(adress): 
    for count_req in range(4):
        
        print("get {}".format(count_req))
        print((await get_massage_from_service(
                domain=adress
            )).get("Response"))
        
        await sleep(2)
    

async def get_adress_facade():
    response_data = await get_massage_from_service(
        domain="http://0.0.0.0:8500",
        url="/v1/catalog/service/api-facade"
    )
    response_data = response_data[0]
    return "http://{adress}:{ports}".format(
        adress=response_data["Address"],
        ports=response_data["ServicePort"]
    )

        
if __name__ == "__main__":
    
    loop = new_event_loop()
    adress = loop.run_until_complete(get_adress_facade())
    loop.run_until_complete(send_message(adress))
    loop.run_until_complete(get_all_massage(adress))
    