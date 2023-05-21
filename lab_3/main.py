from aiohttp import ClientSession, ClientError
import asyncio


async def get_massage_from_service(url: str, method: str, json: dict = None) -> dict:
    async with ClientSession(url) as session:
        async with session.request(url="/", method=method, json=json) as response:
            response.raise_for_status()
            return await response.json()
        

async def send_message():
    for number in range(15):
    
        await get_massage_from_service(
                url="http://0.0.0.0:8015",
                method="POST",
                json={
                    "message": f"messgae num {number}"
                }
            )


async def get_all_massage(): 
    print(await get_massage_from_service(
            url="http://0.0.0.0:8015",
            method="GET"
        ))

        
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(send_message())
    loop.run_until_complete(get_all_massage())
    