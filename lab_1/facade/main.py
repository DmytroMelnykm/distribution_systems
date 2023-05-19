from fastapi import FastAPI
import aiohttp
from modal_body import GetMessage
import uuid
from os import environ
from ports_logger import LoggerPorts


app = FastAPI()


async def get_massage_from_service(url: str, method: str, json: dict = None) -> dict:
    async with aiohttp.ClientSession(url) as session:
        async with session.request(url="/", method=method, json=json) as response:
            response.raise_for_status()
            return await response.json()


@app.get("/")
async def plus_strings():
    
    message_from_message = await get_massage_from_service(
        url=f"http://api-message:{environ.get('PORT_MESSAGE')}",
        method="GET"
    )
    
    #list_message_from_log = await get_massage_from_service()

    # message_from_message = message_from_message["Response"]
    # for message_from_log in list_message_from_log["Response"]:
    #     message_from_message += message_from_log
    
    return {"Response": "message_from_message {}".format(
        message_from_message.get("Response")
        )}


@app.post("/")
async def save_message(data: GetMessage):
    
    await get_massage_from_service(
        url=LoggerPorts.choose_service(),
        method="POST",
        json={
           "message": data.message,
           "uuid": str(uuid.uuid4())
        }
    )
        
    return {"Response": data.message}
