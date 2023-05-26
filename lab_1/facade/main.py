from fastapi import FastAPI
import aiohttp
from modal_body import GetMessage
import uuid
from os import environ
from ports_logger import LoggerPorts


app = FastAPI()


@app.get("/")
async def plus_strings():
    
    message_from_message = (await LoggerPorts.get_massage_from_service(
        url=f"http://api-message:{environ.get('PORT_MESSAGE')}",
        method="GET"
    )).get("Response")
    
    list_message_from_log = (await LoggerPorts.get_massage_from_service(
        url=await LoggerPorts.choose_service(),
        method="GET"
    )).get("Response")
    
    for messgae_from_log in list_message_from_log:
        message_from_message += messgae_from_log

    return {"Response": "{}".format(
        message_from_message
        )}


@app.post("/")
async def save_message(data: GetMessage):
    
    await LoggerPorts.get_massage_from_service(
        url=await LoggerPorts.choose_service(),
        method="POST",
        json={
           "message": data.message,
           "uuid": str(uuid.uuid4())
        }
    )
        
    return {"Response": data.message}
