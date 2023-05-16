from fastapi import FastAPI
import aiohttp
import os
from modal_body import GetMessage
import uuid


app = FastAPI()


async def get_massage_from_service(url: str) -> dict:
    async with aiohttp.ClientSession(url) as session:
        async with session.get("/") as response:
            response.raise_for_status()
            return await response.json()


@app.get("/")
async def plus_strings():
    
    # message_from_message = await get_massage_from_service(os.environ.get("URL_MESSAGE_MACHINE"))
    
    # list_message_from_log = await get_massage_from_service(os.environ.get("URL_LOGGIN_MACHINE"))

    # message_from_message = message_from_message["Response"]
    # for message_from_log in list_message_from_log["Response"]:
    #     message_from_message += message_from_log
    
    return {"Response": "message_from_message"}


@app.post("/")
async def save_message(data: GetMessage):
    
    # async with aiohttp.ClientSession(os.environ.get("URL_LOGGIN_MACHINE")) as session:
    #     async with session.post(
    #         "/", 
    #         json={
    #             "message": data.message, 
    #             "uuid": str(uuid.uuid4())
    #             }
    #         ) as response:
    #         response.raise_for_status()
    
    return {"Response": data.message}
